# Lab 4-2. 이상탐지·예지보전 모델 실습

> 책 4장 4.3절 참고 · 입력: `data/processed/temp_forecast.csv`(Lab 4-1), `data/processed/quality_checked.csv`

## 목표
- Lab 4-1의 예측-실제 잔차와 다른 지표를 결합해 이상 징후(예지보전 필요 후보)를 탐지한다

## 준비물
- `data/processed/temp_forecast.csv` (Lab 4-1 산출물)
- `data/processed/quality_checked.csv` (volt, curr 지표)
- `scikit-learn`

## 단계별 절차
```bash
python ch04_ai_analysis/lab4-2_anomaly_detection/detect_anomaly.py
```
1. 잔차 계산: `residual = temp_c_actual - temp_c_pred` — 클수록 "모델이 예상하지 못한 움직임"
2. 같은 시간대의 `volt`, `curr`를 붙여 특징 확장 — 온도 잔차만으로는 원인을 알 수 없지만, 전압·전류 변화와 함께 보면 "과열"인지 "과부하"인지 구분할 단서가 생긴다
3. `IsolationForest`로 다변량 이상 스코어 산출 → `data/processed/anomaly_flags.csv`

## 결과 확인
```
flagged N / M points as anomaly
saved: .../data/processed/anomaly_flags.csv
```
- `is_anomaly=True` 시점이 잔차(`residual`)가 특히 큰 구간과 대체로 겹치는지 확인한다
- 3장 Lab 3-1에서 IQR로 잡았던 이상치 시점과 비교해본다 — 3장은 단일 지표 기준, 이번은 여러 지표를 함께 본 결과라 완전히 같지는 않을 수 있다

## 트러블슈팅
- `contamination`을 실제보다 크게 잡으면 정상적인 운영 변동까지 이상으로 flag된다 — 작은 값(1~3%)에서 시작해 조정한다
- 잔차와 원본 지표의 스케일 차이가 크면 성능이 떨어질 수 있다 — 필요하면 `StandardScaler`로 맞춘 뒤 학습한다
- `temp_forecast.csv`가 없다는 오류가 나면 Lab 4-1을 먼저 실행했는지 확인한다
