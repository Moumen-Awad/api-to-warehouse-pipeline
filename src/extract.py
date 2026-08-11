import requests
import json
import os
import time
from datetime import datetime, timezone

RAW_DIRECTORY = "raw"
os.makedirs(RAW_DIRECTORY, exist_ok=True)

def fetch_market_data(vs_currency="usd", per_page=100, page=1):
    """
    Calls CoinGeko API and returns a list of coin market data.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cpa_desc",
        "per_page": per_page,
        "page": page
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def save_raw(data, filename_prefix="coin_markets"):
    """
    Saves the raw API response to a timestamped JSON file.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filepath = os.path.join(RAW_DIRECTORY, f"{filename_prefix}_{timestamp}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved{len(data)} records to {filepath}")

if __name__ == "__main__":
    all_data = []
    current_page = 1
    max_pages = 5 # Free API Limit

    print("Starting ingestion process ...")

    while current_page <= max_pages:
        print(f"Fetnching page {current_page} ...")

        page_data = fetch_market_data(page=current_page)

        if not page_data:
            print(f"No more data to be fetched, Stopping at page {current_page}")
            break
        all_data.extend(page_data)

        current_page += 1

    if all_data:
        save_raw(all_data)