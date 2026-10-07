# Project: CAD Exchange Rate Summary
This program downloads CAD exchange rate data and summarizes monthly average and largest rate change for USD, EUR and GBP.
## Data source
The URL: https://api.frankfurter.dev/v1/""2024-01-01..2024-06-30?from=CAD&to=USD,EUR,GBP,
One record represents: {'date': '2024-06-28', 'rates': {'EUR': 0.68166, 'GBP': 0.57695, 'USD': 0.72972} 
128 records return.
## Setup
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
## Run
python records.py
## Example output
Example:
"monthly_averages": {
    "2024-01": {
      "USD": 0.74535,
      "EUR": 0.683487,
      "GBP": 0.586931
    },
    "largest_rate_changes": {
    "USD": 0.00691,
    "EUR": 0.00546,
    "GBP": 0.00781}
## Data quirks
If a record is before our requested start date (2024-01-01), skip it.
## Design choices
We use a list for records = [] because we have many daily exchange-rate records and want to keep them in sequence.
We use dictionaries for several things because each month can be used as a key to quickly access the records belonging to that month. 
We use set to automatically keeps only unique currency codes.
The program is separated into small functions so downloading, cleaning, aggregating, building the summary, and writing the output each have one clear responsibility.
## Known limitations
Depend on the API and internet.
Missing values are skipped, not estimated.
Currencies and date range are fixed by the current program.