import json 
import os
from dotenv import load_dotenv
import glob
from sqlalchemy import create_engine, text

from utils import get_logger, fetch_with_retry

logger = get_logger(__name__)

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "moumen_warehouse")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    return create_engine(DB_URL)

def create_staging_table(engine):
    def _create():
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS staging.coins_markets_raw (
                    id SERIAL PRIMARY KEY,
                    loaded_at TIMESTAMP DEFAULT now(),
                    source_file TEXT,
                    payload JSONB
                );
            """))
            conn.commit()

    logger.info("Ensuring staging table exists...")
    fetch_with_retry(_create, logger=logger)

def load_file(engine, filepath):
    with open(filepath) as f:
        data = json.load(f)

    def _insert():
        with engine.connect() as conn:
            for record in data:
                conn.execute(
                    text("INSERT INTO staging.coins_markets_raw (source_file, payload) VALUES (:src, :payload)"),
                    {"src": os.path.basename(filepath), "payload": json.dumps(record)}
                )
            conn.commit()

    fetch_with_retry(_insert, logger=logger)
    logger.info(f"Loaded {len(data)} records from {filepath}")


if __name__ == "__main__":
    logger.info("Starting database load process...")
    engine = get_engine()
    create_staging_table(engine)

    raw_dir = os.path.join(os.environ.get("AIRFLOW_HOME", "."), "include", "raw")
    files = glob.glob(os.path.join(raw_dir, "*.json"))

    if not files:
        logger.warning(f"No raw files found in {raw_dir}")

    for filepath in files:
        try:
            load_file(engine, filepath)
        except Exception as e:
            logger.error(f"Failed to load file {filepath}: {e}")

    logger.info("Loading process finished.")