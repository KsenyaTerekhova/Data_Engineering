import pandas as pd
from datetime import datetime
import logging

def transform_rates(raw_data: dict) -> pd.DataFrame:
    """Превращает JSON в плоскую таблицу."""
    base = raw_data["base_code"]
    rates = raw_data["rates"]
    
    # Получаем дату обновления из API
    update_date = raw_data.get("time_last_update_utc")
    rate_date = datetime.strptime(update_date, "%a, %d %b %Y %H:%M:%S %z").date()
    
    rows = []
    for currency, rate in rates.items():
        rows.append({
            "base_currency":   base,
            "target_currency": currency,
            "rate":            float(rate),
            "rate_date":       rate_date,
        })
    
    df = pd.DataFrame(rows)
    
    # Очистка: убираем дубли, NaN, отрицательные значения
    df = df.drop_duplicates(subset=["base_currency", "target_currency", "rate_date"])
    df = df.dropna(subset=["rate"])
    df = df[df["rate"] > 0]
    
    logging.info(f"Трансформация завершена: {len(df)} строк")
    return df

if __name__ == "__main__":
    from extract import extract_rates
    df = transform_rates(extract_rates())
    print(df.head())
    print(df.dtypes)
