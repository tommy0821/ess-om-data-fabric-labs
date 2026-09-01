"""quality_checked.csv를 Postgres 테이블(ess_readings)로 적재한다. docker compose up이 먼저 되어 있어야 한다."""
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "processed" / "quality_checked.csv"
DB_URL = "postgresql+psycopg2://postgres:esspass@localhost:5432/postgres"


def main():
    df = pd.read_csv(CSV_PATH)
    engine = create_engine(DB_URL)
    df.to_sql("ess_readings", engine, if_exists="replace", index=False)
    print(f"loaded {len(df):,} rows into ess_readings")


if __name__ == "__main__":
    main()
