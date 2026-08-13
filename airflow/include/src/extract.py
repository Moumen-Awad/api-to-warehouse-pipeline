import requests
import json
import os
from datetime import datetime, timezone

from utils import get_logger, fetch_with_retry

logger = get_logger(__name__)

RAW_DIRECTORY = os.path.join(os.environ.get("AIRFLOW_HOME", "."), "include", "raw")

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

    def _request():
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    return fetch_with_retry(_request, logger=logger)

def save_raw(data, filename_prefix="coin_markets"):
    """
    Saves the raw API response to a timestamped JSON file.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filepath = os.path.join(RAW_DIRECTORY, f"{filename_prefix}_{timestamp}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved {len(data)} records to {filepath}")

if __name__ == "__main__":
    all_data = []
    current_page = 1
    max_pages = 5 # Free API Limit

    logger.info("Starting ingestion process ...")

    while current_page <= max_pages:
        logger.info(f"Fetching page {current_page} ...")

        try:
            page_data = fetch_market_data(page=current_page)
        except Exception as e:
            logger.error(f"Stopping execution due to unhandled error on page {current_page}: {e}")
            break

        if not page_data:
            logger.info(f"No more data to be fetched, Stopping at page {current_page}")
            break

        all_data.extend(page_data)
        current_page += 1

    if all_data:
        save_raw(all_data)
        logger.info("Ingestion completed successfully.")
    else:
        logger.warning("No data was fetched during this run.")