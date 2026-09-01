"""PCS 온도(temp_c) 시계열을 학습해서 다음 시점 값을 예측하는 LSTM 모델.
저장소 루트에서: python ch04_ai_analysis/lab4-1_timeseries_forecast/train_forecast.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from tensorflow.keras import layers

ROOT = Path(__file__).resolve().parents[2]
IN_PATH = ROOT / "data" / "processed" / "quality_checked.csv"
OUT_PATH = ROOT / "data" / "processed" / "temp_forecast.csv"

WINDOW = 12  # 과거 12스텝(5분 간격이면 1시간)으로 다음 1스텝을 예측


def load_series() -> pd.DataFrame:
    df = pd.read_csv(IN_PATH, parse_dates=["ts"])
    return (
        df[(df["device_id"] == "PCS-01") & (df["metric"] == "temp_c")]
        .sort_values("ts")[["ts", "value"]]
        .dropna()
        .reset_index(drop=True)
    )


def make_windows(values: np.ndarray, window: int):
    X, y = [], []
    for i in range(len(values) - window):
        X.append(values[i : i + window])
        y.append(values[i + window])
    return np.array(X), np.array(y)


def main():
    temp = load_series()

    scaler = MinMaxScaler()
    values = scaler.fit_transform(temp[["value"]])

    X, y = make_windows(values, WINDOW)
    split = int(len(X) * 0.8)  # 시간순 분할 — 뒤 20%를 test로
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = keras.Sequential([
        layers.Input(shape=(WINDOW, 1)),
        layers.LSTM(16),
        layers.Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=2)

    pred = model.predict(X_test)
    pred_c = scaler.inverse_transform(pred)
    actual_c = scaler.inverse_transform(y_test)

    mae = float(np.mean(np.abs(pred_c - actual_c)))
    print(f"MAE: {mae:.2f} °C")

    result = temp.iloc[-len(y_test):].copy()
    result["temp_c_pred"] = pred_c
    result["temp_c_actual"] = actual_c
    result.to_csv(OUT_PATH, index=False)
    print(f"saved: {OUT_PATH} ({len(result):,} rows)")


if __name__ == "__main__":
    main()
