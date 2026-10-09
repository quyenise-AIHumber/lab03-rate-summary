import unittest

from ratesummary.models import ExchangeRateRecord


class TestExchangeRateRecord(unittest.TestCase):

    def test_valid_record(self):
        record = ExchangeRateRecord(
            "2024-01-02",
            {"USD": "0.74", "EUR": "0.68", "GBP": "0.58"}
        )

        self.assertEqual(record.date, "2024-01-02")
        self.assertEqual(record.rates["USD"], 0.74)

    def test_missing_currency(self):
        with self.assertRaises(ValueError):
            ExchangeRateRecord(
                "2024-01-02",
                {"USD": 0.74, "EUR": 0.68}
            )

if __name__ == "__main__":
    unittest.main()