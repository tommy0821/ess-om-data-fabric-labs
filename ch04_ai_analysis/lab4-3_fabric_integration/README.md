# Lab 4-3. 분석 결과를 데이터 패브릭에 연계하는 미니 통합 실습

> 책 4장 4.4절 참고 · 입력: `data/processed/temp_forecast.csv`, `data/processed/anomaly_flags.csv`

## 목표
- Lab 4-1(예측)과 Lab 4-2(이상탐지) 결과를 2장의 표준 스키마(`site_id, device_id, device_type, ts, metric, value`)로 되돌려, 원본 센서값과 AI 분석 결과를 같은 카탈로그에서 함께 조회할 수 있게 만든다

## 준비물
- `data/processed/temp_forecast.csv`, `data/processed/anomaly_flags.csv`, `data/processed/unified_long.csv`
- 2장 표준 스키마 (`ch02_integration/lab2-2_schema_standardization/README.md` 참고)

## 단계별 절차
```bash
python ch04_ai_analysis/lab4-3_fabric_integration/integrate_to_fabric.py
```
1. 예측값(`temp_c_pred`)과 이상 스코어(`anomaly_score`)를 새 `metric` 이름(`temp_c_forecast`, `anomaly_score`)을 가진 롱 포맷 레코드로 변환
2. 기존 `unified_long.csv`와 concat → `data/processed/unified_long_with_ai.csv`
3. `metadata_catalog_additions.yaml`의 내용을 `ch02_integration/lab2-2_schema_standardization/metadata_catalog.yaml`에 합쳐 넣는다(수동으로 복사하거나, 두 파일을 합치는 스크립트를 직접 작성해봐도 좋다)

## 결과 확인
```
saved: .../data/processed/unified_long_with_ai.csv (N rows)
metrics: ['anomaly_score', 'cell_temp_max', 'curr', 'soc_pct', 'temp_c', 'temp_c_forecast', 'volt']
```
- `unified_long_with_ai.csv`에서 `metric == "temp_c_forecast"`, `metric == "anomaly_score"`로 필터링하면 원본 센서값과 나란히 같은 파일 안에서 조회되는지 확인한다
- 이 결과가 책 1장 그림 1-1의 "AI 분석/예지보전 → 대시보드·리포트" 화살표가 실제로 완성된 형태다

## 다음 단계
[5장 종합 미니 프로젝트](../../ch05_capstone/README.md)에서 이 파일을 포함해 2~4장 전체 산출물을 하나의 파이프라인으로 잇는다.
