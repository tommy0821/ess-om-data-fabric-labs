"""pcs_raw.csv / bms_raw.csv를 표준 스키마(site_id, device_id, device_type, ts, metric, value)의
롱 포맷으로 통합한다. 저장소 루트에서: python ch02_integration/lab2-2_schema_standardization/standardize.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"


def standardize_pcs(path: Path) -> pd.DataFrame:
    pcs = pd.read_csv(path)
    pcs["ts"] = pd.to_datetime(pcs["ts"]).dt.tz_localize("Asia/Seoul").dt.tz_convert("UTC")
    long = pcs.melt(
        id_vars=["ts", "device"], value_vars=["volt", "curr", "temp_c"],
        var_name="metric", value_name="value",
    ).rename(columns={"device": "device_id"})
    long["device_type"] = "PCS"
    return long


def standardize_bms(path: Path) -> pd.DataFrame:
    bms = pd.read_csv(path)
    bms["ts"] = pd.to_datetime(bms["timestamp"]).dt.tz_convert("UTC")
    long = bms.melt(
        id_vars=["ts", "unit_id"], value_vars=["soc_pct", "cell_temp_max"],
        var_name="metric", value_name="value",
    ).rename(columns={"unit_id": "device_id"})
    long["device_type"] = "BMS"
    return long


def main():
    pcs_long = standardize_pcs(RAW_DIR / "pcs_raw.csv")
    bms_long = standardize_bms(RAW_DIR / "bms_raw.csv")

    unified = pd.concat([pcs_long, bms_long], ignore_index=True)
    unified["site_id"] = "site_A"
    unified = unified[["site_id", "device_id", "device_type", "ts", "metric", "value"]]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "unified_long.csv"
    unified.to_csv(out_path, index=False)
    print(f"saved: {out_path} ({len(unified):,} rows)")
    print("metrics:", sorted(unified["metric"].unique()))


if __name__ == "__main__":
    main()
