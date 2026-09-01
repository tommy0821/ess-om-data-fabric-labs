"""Lab 4-1의 예측-실제 잔차와 volt/curr 지표를 결합해 IsolationForest로 이상 징후(예지보전 후보)를 탐지한다.
저장소 루트에서: python ch04_ai_analysis/lab4-2_anomaly_detection/detect_anomaly.py
"""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parents[2]
FORECAST_PATH = ROOT / "data" / "processed" / "temp_forecast.csv"
QUALITY_PATH = ROOT / "data" / "processed" / "quality_checked.csv"
OUT_PATH = ROOT / "data" / "processed" / "anomaly_flags.csv"


def main():
    forecast = pd.read_csv(FORECAST_PATH, parse_dates=["ts"])
    forecast["residual"] = forecast["temp_c_actual"] - forecast["temp_c_pred"]

    df = pd.read_csv(QUALITY_PATH, parse_dates=["ts"])
    wide = df[df["device_id"] == "PCS-01"].pivot_table(index="ts", columns="metric", values="value")

    features = forecast.set_index("ts")[["residual"]].join(wide[["volt", "curr"]], how="inner")

    X = features[["residual", "volt", "curr"]]
    model = IsolationForest(contamination=0.03, random_state=0)
    features["is_anomaly"] = model.fit_predict(X) == -1        # 먼저 학습+예측
    features["anomaly_score"] = model.decision_function(X)     # 학습된 모델로 스코어 산출 (낮을수록 이상)

    print(f"flagged {int(features['is_anomaly'].sum())} / {len(features)} points as anomaly")

    features.reset_index().to_csv(OUT_PATH, index=False)
    print(f"saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
