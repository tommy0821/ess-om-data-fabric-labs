"""IQR(통계) + IsolationForest(ML) 두 방식으로 이상치를 탐지·비교하고,
결측 보간·중복 제거까지 마친 정제 데이터셋을 만든다. inject_noise.py를 먼저 실행해야 한다.
"""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parents[2]
IN_PATH = ROOT / "data" / "processed" / "unified_long_noisy.csv"
OUT_PATH = ROOT / "data" / "processed" / "quality_checked.csv"


def flag_iqr(group: pd.DataFrame, k: float = 1.5) -> pd.Series:
    q1, q3 = group["value"].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return (group["value"] < lower) | (group["value"] > upper)


def count_isolation_forest_flags(df: pd.DataFrame) -> int:
    """지표들을 와이드 포맷으로 펼쳐서, 여러 지표의 조합 패턴을 함께 보는 다변량 이상치 탐지.
    (device_id, ts) 중복이 있으면 pivot_table이 평균을 취하므로, dedup 이전 단계에서만 참고용으로 쓴다."""
    wide = df.pivot_table(index=["device_id", "ts"], columns="metric", values="value").reset_index()
    features = wide.drop(columns=["device_id", "ts"])

    model = IsolationForest(contamination=0.01, random_state=0)
    flags = model.fit_predict(features.fillna(features.mean())) == -1
    return int(flags.sum())


def main():
    df = pd.read_csv(IN_PATH, parse_dates=["ts"])

    df["is_outlier_iqr"] = df.groupby("metric", group_keys=False).apply(flag_iqr)
    if_flag_count = count_isolation_forest_flags(df)
    print(f"IQR flagged: {int(df['is_outlier_iqr'].sum())} rows, IsolationForest flagged: {if_flag_count} (device,ts) combos")

    df = df.sort_values(["device_id", "metric", "ts"])
    df["value"] = df.groupby(["device_id", "metric"])["value"].transform(lambda s: s.interpolate())
    df = df.drop_duplicates(subset=["device_id", "ts", "metric"])
    df["is_outlier"] = df["is_outlier_iqr"]  # 최종 플래그는 IQR 결과를 채택(간단한 예시)

    df.to_csv(OUT_PATH, index=False)
    print(f"saved: {OUT_PATH} ({len(df):,} rows)")


if __name__ == "__main__":
    main()
