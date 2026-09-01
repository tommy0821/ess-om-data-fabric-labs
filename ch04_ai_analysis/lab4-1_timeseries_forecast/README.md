# Lab 4-1. 배터리 온도/성능 시계열 예측 모델 실습

> 책 4장 4.2절 참고 · 입력: `data/processed/quality_checked.csv` (3장 산출물)

## 목표
- PCS 온도(`temp_c`) 시계열을 학습해서 다음 시점 값을 예측하는 LSTM 모델을 만든다

## 준비물
- `data/processed/quality_checked.csv`
- `tensorflow`(Keras 포함), `scikit-learn` (저장소 루트 `requirements.txt`에 포함됨)

## 단계별 절차
```bash
python ch04_ai_analysis/lab4-1_timeseries_forecast/train_forecast.py
```
스크립트는 다음을 순서대로 수행한다.
1. `PCS-01`의 `temp_c` 시계열만 추출·정렬
2. `MinMaxScaler`로 정규화
3. 슬라이딩 윈도우 생성(과거 12스텝 → 다음 1스텝)
4. 시간순으로 train(80%)/test(20%) 분할
5. Keras LSTM 모델 학습
6. 예측값을 역정규화해서 `data/processed/temp_forecast.csv`로 저장 — 4-2, 4-3 Lab의 입력이 된다

## 결과 확인
```
MAE: X.XX °C
saved: .../data/processed/temp_forecast.csv (N rows)
```
- `temp_forecast.csv`의 `temp_c_pred`(예측)와 `temp_c_actual`(실제)을 그래프로 그려서 예측 곡선이 실제값의 추세를 따라가는지 확인한다
- MAE가 온도 변동 폭에 비해 합리적인 수준인지 확인한다(수십 배 차이가 나면 정규화·윈도우 크기를 점검)

## 트러블슈팅
- LSTM 입력 shape 오류가 가장 흔하다 — `(batch, timesteps, features)` 3차원을 기대한다(`train_forecast.py`의 `Input(shape=(WINDOW, 1))` 참고)
- 이 실습에서는 데이터 규모가 작아 `MinMaxScaler`를 전체 구간에 `fit_transform`했다 — 실무에서는 train 구간에만 `fit`하고 test에는 `transform`만 적용하는 것이 원칙이다
