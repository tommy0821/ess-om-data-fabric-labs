# Lab 3-1. 이상치 탐지·데이터 정제 스크립트 작성 및 적용

> 책 3장 3.2절 참고 · 입력: `data/processed/unified_long.csv` (Lab 2-2 산출물)

## 목표
- 통계적 방법(IQR)과 머신러닝 방법(IsolationForest)으로 각각 이상치를 탐지하고 결과를 비교한다
- 결측·중복·이상치를 정리한 정제 데이터셋을 만든다

## 준비물
- `data/processed/unified_long.csv` (Lab 2-2 산출물)
- `scikit-learn`

## 단계별 절차
1. 1장 기본 생성기로 만든 데이터는 이상치가 없으므로, 실습용 이상치를 인위적으로 주입한다.
   ```bash
   python ch03_quality_security/lab3-1_outlier_detection/inject_noise.py
   ```
2. IQR + IsolationForest 두 방식으로 탐지하고, 결측 보간·중복 제거까지 마친 정제 데이터셋을 만든다.
   ```bash
   python ch03_quality_security/lab3-1_outlier_detection/detect_outliers.py
   ```

## 결과 확인
```
IQR flagged: N rows, IsolationForest flagged: M (device,ts) combos
saved: .../data/processed/quality_checked.csv (K rows)
```
- `quality_checked.csv`에 `is_outlier` 컬럼이 있고, `inject_noise.py`가 주입한 지점 근처에서 `True`가 잡히는지 확인한다
- 원본 대비 결측치 개수(`isna().sum()`)와 중복 행 수가 줄었는지 확인한다
- 이상치를 곧바로 삭제하지 않고 플래그만 남긴 이유: 실제로는 이상치처럼 보이는 값이 진짜 설비 이상 징후일 수 있다 — 이 판단은 4장(AI 기반 예지보전)에서 다시 다룬다

## 트러블슈팅
- `pivot_table`에서 `(device_id, ts)` 조합이 중복되면 값이 평균으로 뭉개질 수 있다 — dedup을 IsolationForest 적용보다 먼저 하고 싶다면 순서를 바꿔서 실행한다
- `IsolationForest`의 `contamination`을 실제 이상치 비율보다 크게 잡으면 정상값도 과도하게 이상치로 분류된다
- `unified_long_noisy.csv`가 없다는 오류가 나면 `inject_noise.py`를 먼저 실행했는지 확인한다
