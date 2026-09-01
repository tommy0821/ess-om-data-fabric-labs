import numpy as np
import pandas as pd

idx = pd.date_range("2026-01-01", periods=30 * 288, freq="5min")  # 30일 x 5분 간격

# PCS: ts, device, volt, curr, temp_c, status_code
pcs = pd.DataFrame({
    "ts": idx.strftime("%Y-%m-%d %H:%M:%S"),
    "device": "PCS-01",
    "volt": np.random.normal(380, 3, len(idx)),
    "curr": np.random.normal(0, 40, len(idx)),
    "temp_c": np.random.normal(28, 3, len(idx)),
    "status_code": 0,
})

# BMS: PCS와 컬럼명·타임스탬프 포맷을 의도적으로 다르게
bms = pd.DataFrame({
    "timestamp": idx.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
    "unit_id": "BMS-01",
    "soc_pct": np.random.uniform(20, 90, len(idx)),
    "cell_temp_max": np.random.normal(29, 2, len(idx)),
})

pcs.to_csv("../data/raw/pcs_raw.csv", index=False)
bms.to_csv("../data/raw/bms_raw.csv", index=False)