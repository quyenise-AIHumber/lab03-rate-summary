import json
from pathlib import Path
import requests

SOURCE_URL = (
    "https://api.frankfurter.dev/v1/"
    "2024-01-01..2024-06-30?from=CAD&to=USD,EUR,GBP"
)

OUTPUT = Path("summary.json")

def fetch_rates(url):
    """Download exchange-rate data from the API."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["rates"] 

def clean_rates(rates):
    """Remove records before 2024-01-01."""
    records = []
    for date_text, daily_rates in rates.items():
        if date_text < "2024-01-01":
            continue  
        records.append({"date": date_text, "rates": daily_rates})
    return records


def monthly_average_rates(grouped):
    """Calculate the monthly average for each currency."""
    currencies = ["USD", "EUR", "GBP"]
    monthly_averages = {}
    for month, month_records in grouped.items():
        monthly_averages[month]= {}
        
        for currency in currencies:
            values = []
            for record in month_records:
                rate = record["rates"][currency]
                values.append(rate)
            average = round(sum(values) / len(values), 6)
            monthly_averages[month][currency] = average
    return monthly_averages

def group_by_month(records):
    """Group exchange-rate records by month."""
    grouped = {}
    for record in records:
        month = record["date"][:7]  # Extract YYYY-MM
        if month not in grouped:
            grouped[month] = []
        grouped[month].append(record)
    return grouped

def largest_rate_changes(records):
    """Identify the largest rate changes for each currency."""
    records = sorted(records, key=lambda record: record["date"])
    
    currencies = ["USD", "EUR", "GBP"]
    largest_changes = {}
    for currency in currencies:
        previous_rate = None
        largest_change = 0
        
        for record in records:
            current_rate = record["rates"][currency]
            if previous_rate is not None:
                change = current_rate - previous_rate
                absolute_change = abs(change)
                if absolute_change > largest_change:
                    largest_change = absolute_change
            previous_rate = current_rate
        largest_changes[currency] = round(largest_change, 6)
    
    return largest_changes


def build_summary(records, currency_found, monthly_averages, largest_changes):
    """Build the final summary dictionary."""
    summary = {
        "source": SOURCE_URL,
        "records_processed": len(records),
        "currencies_found": sorted(currency_found),
        "monthly_averages": monthly_averages,
        "largest_rate_changes": largest_changes
    }
    return summary


def write_summary_to_file(summary, output_path):
    """Write the summary dictionary to a JSON file."""
    json_text = json.dumps(summary, indent=2)
    output_path.write_text(json_text, encoding="utf-8")

def main():
    try: 
            rates = fetch_rates(SOURCE_URL)
            
    except requests.RequestException as error:
            print(f"Error fetching rates: {error}")
            return  
    
    records = clean_rates(rates)
    grouped = group_by_month(records)
    monthly_averages = monthly_average_rates(grouped)
    largest_changes = largest_rate_changes(records)
    currency_found = {
        currency
        for record in records
        for currency in record["rates"]
    }
    summary = build_summary(records, currency_found, monthly_averages, largest_changes)
    write_summary_to_file(summary, OUTPUT)
    

if __name__ == "__main__":
    main()   