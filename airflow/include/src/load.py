import json 
import os
from dotenv import load_dotenv
import glob
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "moumen")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "moumen_db_sec_2026")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "moumen_warehouse")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    return create_engine(DB_URL)

def create_staging_table(engine):
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

def load_file(engine, filepath):
    with open(filepath) as f:
        data = json.load(f)
    with engine.connect() as conn:
        for record in data:
            conn.execute(
                text("INSERT INTO staging.coins_markets_raw (source_file, payload) VALUES (:src, :payload)"),
                {"src": os.path.basename(filepath), "payload": json.dumps(record)}
            )
        conn.commit()
    print(f"Loaded {len(data)} records from {filepath}")


if __name__ == "__main__":
    engine = get_engine()
    create_staging_table(engine)
    for filepath in glob.glob("raw/*.json"):
        load_file(engine,filepath)