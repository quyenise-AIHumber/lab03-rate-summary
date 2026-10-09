class ExchangeRateRecord:
    """Represent one daily exchange-rate record."""

    def __init__(self, date, rates):
        if not date:
            raise ValueError("Date is required.")

        if not isinstance(rates, dict):
            raise ValueError("Rates must be a dictionary.")

        required_currencies = ["USD", "EUR", "GBP"]

        cleaned_rates = {}

        for currency in required_currencies:
            if currency not in rates:
                raise ValueError(f"Missing currency: {currency}")

            try:
                cleaned_rates[currency] = float(rates[currency])
            except (TypeError, ValueError):
                raise ValueError(f"Invalid rate for {currency}")

        self.date = str(date).strip()
        self.rates = cleaned_rates

    def __str__(self):
        return f"{self.date}: {self.rates}"