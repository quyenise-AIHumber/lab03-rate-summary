class Aggregation:
    """Base class for exchange-rate aggregations."""

    def calculate(self, records):
        raise NotImplementedError("Subclasses must implement calculate().")

class MonthlyAverageAggregation(Aggregation):
    """Calculate monthly average exchange rates."""

    def calculate(self, records):
        currencies = ["USD", "EUR", "GBP"]
        grouped = {}

        for record in records:
            month = record.date[:7]

            if month not in grouped:
                grouped[month] = []

            grouped[month].append(record)

        monthly_averages = {}

        for month, month_records in grouped.items():
            monthly_averages[month] = {}

            for currency in currencies:
                values = []

                for record in month_records:
                    values.append(record.rates[currency])

                average = round(sum(values) / len(values), 6)
                monthly_averages[month][currency] = average

        return monthly_averages

class LargestRateChangeAggregation(Aggregation):
    """Calculate the largest daily rate change for each currency."""

    def calculate(self, records):
        records = sorted(records, key=lambda record: record.date)
        currencies = ["USD", "EUR", "GBP"]
        largest_changes = {}

        for currency in currencies:
            previous_rate = None
            largest_change = 0

            for record in records:
                current_rate = record.rates[currency]

                if previous_rate is not None:
                    change = current_rate - previous_rate
                    absolute_change = abs(change)

                    if absolute_change > largest_change:
                        largest_change = absolute_change

                previous_rate = current_rate

            largest_changes[currency] = round(largest_change, 6)

        return largest_changes