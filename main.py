from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
from .database import fetch_rates_by_date

app = FastAPI()

logging.basicConfig(level=logging.INFO)


# Helper function to calculate percentage change
def calculate_change(current_rate: Optional[float], previous_rate: Optional[float]) -> Optional[float]:
    if current_rate is not None and previous_rate is not None and previous_rate != 0:
        return ((current_rate - previous_rate) / previous_rate) * 100
    return None


@app.get("/")
def read_root():
    return {"message": "Currency Rates API"}


@app.get("/rates/compare")
def get_current_and_previous_rates() -> Dict[str, Any]:
    # Get today's date in 'YYYY-MM-DD' format
    today = datetime.strptime('2024-10-16', '%Y-%m-%d').date()

    # Get previous day's date in 'YYYY-MM-DD' format
    previous_day = datetime.strptime('2024-10-15', '%Y-%m-%d').date()

    # Fetch current and previous day rates
    current_rates = fetch_rates_by_date(today)
    previous_rates = fetch_rates_by_date(previous_day)

    if not current_rates:
        raise HTTPException(status_code=404, detail="No rates found for today.")

    if not previous_rates:
        raise HTTPException(status_code=404, detail="No rates found for the previous day.")

    # List of currency columns (based on the keys available in the database)
    currency_columns = ['USD', 'JPY', 'BGN', 'CYP', 'CZK', 'DKK', 'EEK', 'GBP', 'HUF', 'LTL', 'LVL', 'MTL',
                        'PLN', 'ROL', 'RON', 'SEK', 'SIT', 'SKK', 'CHF', 'ISK', 'NOK', 'HRK', 'RUB', 'TRL',
                        'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR',
                        'NZD', 'PHP', 'SGD', 'THB', 'ZAR']

    rate_comparisons = []

    for currency in currency_columns:
        # Access current and previous rates, ensuring the column exists
        current_rate = current_rates[0][currency] if currency in current_rates[0].keys() else None
        previous_rate = previous_rates[0][currency] if currency in previous_rates[0].keys() else None

        rate_comparisons.append({
            "currency": currency,
            "current_rate": current_rate,
            "previous_rate": previous_rate,
            "rate_change_percentage": calculate_change(current_rate, previous_rate)
        })

    return {"date": today, "comparisons": rate_comparisons}