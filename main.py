
from ratesummary.sources import ExchangeRateSource, SourceError
from ratesummary.report import build_summary, write_summary
from ratesummary.config import SOURCE_URL, TIMEOUT, OUTPUT_PATH

def main():
    """Run the exchange-rate summary program."""

    source = ExchangeRateSource(SOURCE_URL, timeout=TIMEOUT)

    try:
        records = source.fetch()
    except SourceError as error:
        print(f"Error fetching rates: {error}")
        return

    summary = build_summary(records, SOURCE_URL)
    write_summary(summary, OUTPUT_PATH)
    
if __name__ == "__main__":
    main()