"""1장 기본 생성기로 만든 데이터는 이상치가 없으므로, 탐지 기법을 연습할 수 있도록
unified_long.csv에서 값 몇 개를 인위적으로 튀게 만든 사본을 만든다.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
IN_PATH = ROOT / "data" / "processed" / "unified_long.csv"
OUT_PATH = ROOT / "data" / "processed" / "unified_long_noisy.csv"


def main():
    df = pd.read_csv(IN_PATH, parse_dates=["ts"])

    rng = np.random.default_rng(0)
    noisy_idx = rng.choice(df.index, size=8, replace=False)
    df.loc[noisy_idx, "value"] *= rng.uniform(2.5, 4.0, size=8)

    df.to_csv(OUT_PATH, index=False)
    print(f"saved: {OUT_PATH} (noise injected at {len(noisy_idx)} rows: {sorted(noisy_idx)})")


if __name__ == "__main__":
    main()
