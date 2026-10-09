import json

from .aggregations import (
    MonthlyAverageAggregation,
    LargestRateChangeAggregation,
)

def build_aggregation_results(records):
    """Run all aggregations and return their results."""

    aggregations = [
        ("monthly_averages", MonthlyAverageAggregation()),
        ("largest_rate_changes", LargestRateChangeAggregation()),
    ]

    results = {}

    for name, aggregation in aggregations:
        results[name] = aggregation.calculate(records)

    return results

def build_summary(records, source_url):
    """Build the final summary dictionary."""

    aggregation_results = build_aggregation_results(records)

    currencies_found = sorted({
        currency
        for record in records
        for currency in record.rates
    })

    summary = {
        "source": source_url,
        "records_processed": len(records),
        "currencies_found": currencies_found,
        "monthly_averages": aggregation_results["monthly_averages"],
        "largest_rate_changes": aggregation_results["largest_rate_changes"],
    }

    return summary

def write_summary(summary, output_path):
    """Write the summary dictionary to a JSON file."""

    json_text = json.dumps(summary, indent=2)
    output_path.write_text(json_text, encoding="utf-8")