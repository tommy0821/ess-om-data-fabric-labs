"""Lab 2-2의 표준화 로직을 Airflow DAG으로 감싼 버전.
컨테이너 안에서는 저장소 루트 data/ 폴더가 /opt/airflow/data 로 마운트되어 있다(docker-compose.yml 참고).
"""
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

DATA_DIR = Path("/opt/airflow/data")


def standardize():
    pcs = pd.read_csv(DATA_DIR / "raw" / "pcs_raw.csv")
    pcs["ts"] = pd.to_datetime(pcs["ts"]).dt.tz_localize("Asia/Seoul").dt.tz_convert("UTC")
    pcs_long = pcs.melt(
        id_vars=["ts", "device"], value_vars=["volt", "curr", "temp_c"],
        var_name="metric", value_name="value",
    ).rename(columns={"device": "device_id"})
    pcs_long["device_type"] = "PCS"

    bms = pd.read_csv(DATA_DIR / "raw" / "bms_raw.csv")
    bms["ts"] = pd.to_datetime(bms["timestamp"]).dt.tz_convert("UTC")
    bms_long = bms.melt(
        id_vars=["ts", "unit_id"], value_vars=["soc_pct", "cell_temp_max"],
        var_name="metric", value_name="value",
    ).rename(columns={"unit_id": "device_id"})
    bms_long["device_type"] = "BMS"

    unified = pd.concat([pcs_long, bms_long], ignore_index=True)
    unified["site_id"] = "site_A"
    unified = unified[["site_id", "device_id", "device_type", "ts", "metric", "value"]]

    out_dir = DATA_DIR / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    unified.to_csv(out_dir / "unified_long.csv", index=False)


with DAG(
    dag_id="standardize_ess_data",
    start_date=datetime(2026, 1, 1),
    schedule="*/10 * * * *",   # 10분마다 실행
    catchup=False,
) as dag:
    PythonOperator(task_id="standardize", python_callable=standardize)
