"""CLI entry point for the prompt refactoring tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from .analyzer import AnalyzerError, analyze_prompt, refactor_prompt
from .card_builder import build_card
from .config import DEFAULT_MODEL, DEFAULT_REPO_ROOT, ensure_api_key, load_env_file, resolve_repo_root
from .repo_placer import place_card


CLEAR_LABELS = {
    "concise": "Concise",
    "logical": "Logical",
    "explicit": "Explicit",
    "adaptive": "Adaptive",
    "reflective": "Reflective",
}


def _status_icon(note: str) -> str:
    lowered = note.lower()
    if any(word in lowered for word in ("no ", "missing", "not ", "without", "none")):
        return "⚠️ "
    return "✅ "


def read_interactive_prompt() -> str:
    """Read multiline prompt from terminal until double empty line or EOF."""
    print("Paste your prompt (empty line twice or Ctrl+D to finish):")
    lines: list[str] = []
    empty_count = 0
    try:
        while True:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append(line)
            else:
                empty_count = 0
                lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines).strip()


def read_raw_prompt(args: argparse.Namespace) -> str:
    """Load raw prompt text from file, stdin, or interactive input."""
    if args.stdin:
        raw = sys.stdin.read()
        if not raw.strip():
            raise SystemExit("Error: stdin is empty.")
        return raw.strip()

    if args.input:
        path = Path(args.input).expanduser()
        if not path.is_file():
            raise SystemExit(f"Error: input file not found: {path}")
        return path.read_text(encoding="utf-8").strip()

    raw = read_interactive_prompt()
    if not raw:
        raise SystemExit("Error: no prompt provided.")
    return raw


def print_clear_report(refactor: dict[str, Any], analysis: dict[str, Any]) -> None:
    """Print CLEAR assessment summary."""
    print("\n📋 CLEAR Assessment:")
    report = refactor.get("clear_report") or {}
    assessment = analysis.get("clear_assessment") or {}

    for key, label in CLEAR_LABELS.items():
        if key in report:
            note = report[key]
            print(f"  {label + ':':<12} {_status_icon(note)}{note}")
        elif key in assessment:
            item = assessment[key]
            status = item.get("status", "ok")
            note = item.get("note", "")
            icon = "✅" if status == "ok" else "⚠️ "
            print(f"  {label + ':':<12} {icon}{note}")
        else:
            print(f"  {label + ':':<12} ⚠️  Not assessed")


def print_summary(card: dict[str, Any], saved_path: Path, dry_run: bool) -> None:
    """Print final summary after card creation."""
    tags = ", ".join(card.get("tags", []))
    if not dry_run:
        print(f"\n📁 Saved: {saved_path}")
    print(f"🏷  Tags: {tags}")
    print(f"🔖 Version: {card.get('version', '1.0.0')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Refactor a personal prompt into a team YAML card using CLEAR.",
    )
    parser.add_argument(
        "--input",
        help="Path to a file containing the raw prompt",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read raw prompt from stdin",
    )
    parser.add_argument(
        "--owner",
        required=True,
        help="Card owner (e.g. @vadim)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Target model for the prompt card (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--category",
        default="auto",
        help='Category name or "auto" to let the LLM decide (default: auto)',
    )
    parser.add_argument(
        "--mode",
        choices=["draft", "production"],
        default="production",
        help="Refactoring mode (default: production)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the card without writing to disk",
    )
    parser.add_argument(
        "--env-file",
        help="Path to a .env file with OPENAI_API_KEY",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help=f"Prompt library repository root (default: {DEFAULT_REPO_ROOT})",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_root = resolve_repo_root(args.repo_root)
    if not repo_root.is_dir():
        print(f"Error: repository root not found: {repo_root}", file=sys.stderr)
        return 1

    load_env_file(repo_root / ".env")
    if args.env_file:
        load_env_file(Path(args.env_file).expanduser())

    try:
        ensure_api_key()
        raw_prompt = read_raw_prompt(args)

        print("⏳ Analyzing prompt...")
        analysis = analyze_prompt(raw_prompt, category=args.category)

        print("⏳ Refactoring with CLEAR...")
        refactor = refactor_prompt(
            raw_prompt,
            analysis,
            mode=args.mode,
            target_model=args.model,
        )

        category_override = None if args.category == "auto" else args.category
        card, filename = build_card(
            analysis,
            refactor,
            owner=args.owner,
            model=args.model,
            category_override=category_override,
        )

        saved_path, _errors = place_card(
            card,
            filename,
            repo_root=str(repo_root),
            dry_run=args.dry_run,
        )

        print_clear_report(refactor, analysis)
        print_summary(card, saved_path, dry_run=args.dry_run)
        return 0

    except AnalyzerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
