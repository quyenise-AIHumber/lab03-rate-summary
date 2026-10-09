from urllib import response

import requests

from .models import ExchangeRateRecord

class SourceError(Exception):
    """Raised when exchange-rate data cannot be downloaded."""

class ExchangeRateSource:
    """Download exchange-rate data from an API."""

    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout

    def fetch(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            raise SourceError(f"Error fetching rates: {error}") from error
        
        data = response.json()

        records = []

        for date_text, daily_rates in data["rates"].items():
            if date_text < "2024-01-01":
                continue
            record = ExchangeRateRecord(date_text, daily_rates)
            records.append(record)

        return records