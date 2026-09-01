"""Lab 4-1(예측)과 Lab 4-2(이상탐지) 결과를 2장의 표준 스키마로 되돌려, 원본 센서값과
AI 분석 결과를 같은 카탈로그에서 함께 조회할 수 있게 만든다.
저장소 루트에서: python ch04_ai_analysis/lab4-3_fabric_integration/integrate_to_fabric.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
FORECAST_PATH = ROOT / "data" / "processed" / "temp_forecast.csv"
ANOMALY_PATH = ROOT / "data" / "processed" / "anomaly_flags.csv"
UNIFIED_PATH = ROOT / "data" / "processed" / "unified_long.csv"
OUT_PATH = ROOT / "data" / "processed" / "unified_long_with_ai.csv"

COLS = ["site_id", "device_id", "device_type", "ts", "metric", "value"]


def to_standard(df: pd.DataFrame, value_col: str, metric_name: str) -> pd.DataFrame:
    long = df[["ts", value_col]].rename(columns={value_col: "value"})
    long["metric"] = metric_name
    long["site_id"] = "site_A"
    long["device_id"] = "PCS-01"
    long["device_type"] = "PCS"
    return long[COLS]


def main():
    forecast = pd.read_csv(FORECAST_PATH, parse_dates=["ts"])
    anomaly = pd.read_csv(ANOMALY_PATH, parse_dates=["ts"])
    unified = pd.read_csv(UNIFIED_PATH, parse_dates=["ts"])

    forecast_long = to_standard(forecast, "temp_c_pred", "temp_c_forecast")
    anomaly_long = to_standard(anomaly, "anomaly_score", "anomaly_score")

    combined = pd.concat([unified[COLS], forecast_long, anomaly_long], ignore_index=True)
    combined.to_csv(OUT_PATH, index=False)

    print(f"saved: {OUT_PATH} ({len(combined):,} rows)")
    print("metrics:", sorted(combined["metric"].unique()))


if __name__ == "__main__":
    main()
