import json
import logging
import psycopg2
from sqlalchemy import create_engine, text
from config import DB_CONFIG

def load_raw_to_stg(raw_data: dict):
    """Грузим сырой JSON в STG."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO stg.exchange_rates_raw (base_currency, rates_json) VALUES (%s, %s)",
                (raw_data["base_code"], json.dumps(raw_data["rates"]))
            )
    logging.info("STG: сырые данные загружены")

def load_clean_to_dwh(df):
    """Грузим очищенный DataFrame в DWH."""
    engine = create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    
    # ON CONFLICT DO NOTHING защищает от дублей при повторных запусках
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO dwh.exchange_rates (base_currency, target_currency, rate, rate_date)
                    VALUES (:base_currency, :target_currency, :rate, :rate_date)
                    ON CONFLICT (base_currency, target_currency, rate_date) DO NOTHING
                """),
                row.to_dict()
            )
    logging.info(f"DWH: загружено {len(df)} строк")
