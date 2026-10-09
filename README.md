# Exchange Rate Summary

This package summarizes CAD exchange rates for USD, EUR, and GBP.
It calculates monthly average rates and the largest daily rate changes.

## Data source

URL:
https://api.frankfurter.dev/v1/2024-01-01..2024-06-30?from=CAD&to=USD,EUR,GBP

One record represents the exchange rates for one date.

The program processes about 126 records from January 2024 to June 2024.

## Setup

conda env create -f environment.yml

conda activate ratesummary

pip install -r requirements.txt

pip install -e .

## Run

python main.py

The output file is created at:

data/processed/summary.json

## Test

python -m unittest discover -s tests