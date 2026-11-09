import logging
from extract import extract_rates
from transform import transform_rates
from load import load_raw_to_stg, load_clean_to_dwh

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run_pipeline():
    logging.info("=== Старт ETL-пайплайна ===")
    raw = extract_rates()
    load_raw_to_stg(raw)
    df = transform_rates(raw)
    load_clean_to_dwh(df)
    logging.info("=== Пайплайн завершён успешно ===")

if __name__ == "__main__":
    run_pipeline()
