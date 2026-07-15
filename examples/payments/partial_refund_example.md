# Example: payments.partial_refund

## Input

```yaml
product: "Wireless Headphones Pro"
amount: 2500
currency: "RUB"
reason: "Damaged packaging"
receipt_url: "https://store.example.com/receipts/R-20250601-0042"
```

## Expected Output

> We've processed a partial refund of 2,500 RUB for your Wireless Headphones Pro
> due to damaged packaging. You can view your updated receipt here:
> https://store.example.com/receipts/R-20250601-0042. Feel free to reach out
> if you have any questions.
