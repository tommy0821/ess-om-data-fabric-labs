# Lab 2-2. 이기종 데이터 스키마 표준화·메타데이터 통합 실습

> 책 2장 2.3절 참고 · 입력: `data/raw/pcs_raw.csv`, `data/raw/bms_raw.csv` (컬럼명·타임스탬프 포맷이 서로 다르게 설계됨)

## 목표
- 컬럼명·타임스탬프 포맷이 다른 두 원본 파일을 하나의 표준 스키마로 통합한다
- 표준 스키마에 어떤 지표인지 설명해주는 최소한의 메타데이터 카탈로그를 만든다

## 준비물
- `data/raw/pcs_raw.csv`, `data/raw/bms_raw.csv` (`ch01_setup/generate_sample_data.py`로 생성된 파일)
- `pandas`

## 스키마 차이

| | pcs_raw.csv | bms_raw.csv |
|---|---|---|
| 타임스탬프 컬럼 | `ts` (`2026-01-01 00:00:00`) | `timestamp` (`2026-01-01T00:00:00+09:00`) |
| 장비 식별 컬럼 | `device` (`PCS-01`) | `unit_id` (`BMS-01`) |
| 값 컬럼 | `volt, curr, temp_c` | `soc_pct, cell_temp_max` |

## 표준 스키마

| 컬럼 | 설명 |
|---|---|
| `site_id` | 사업장 ID (`site_A`) |
| `device_id` | 장비 ID (`PCS-01`, `BMS-01`) |
| `device_type` | 장비 유형 (`PCS`, `BMS`) |
| `ts` | 타임스탬프, UTC ISO8601로 통일 |
| `metric` | 지표명 (`volt`, `curr`, `temp_c`, `soc_pct`, `cell_temp_max`) |
| `value` | 값 |

## 단계별 절차
1. 저장소 루트에서 실행한다.
   ```bash
   python ch02_integration/lab2-2_schema_standardization/standardize.py
   ```
2. `standardize.py`는 두 원본 CSV를 각각 롱 포맷으로 변환한 뒤(`pandas.melt`) 하나로 합쳐 `data/processed/unified_long.csv`로 저장한다.
3. `metadata_catalog.yaml`에 각 `metric`의 단위·설명이 정의돼 있다 — 대시보드나 AI 모델이 지표를 "해석"할 때 이 파일을 참조한다.

## 결과 확인
```
saved: .../data/processed/unified_long.csv (N rows)
metrics: ['cell_temp_max', 'curr', 'soc_pct', 'temp_c', 'volt']
```
- `unified_long.csv`의 `device_type` 컬럼에 `PCS`와 `BMS`가 함께 있는지
- `ts`가 모두 같은 타임존(UTC)으로 통일됐는지
- 5개 지표(volt, curr, temp_c, soc_pct, cell_temp_max)가 모두 들어왔는지

## 트러블슈팅
- 타임존 변환 시 `tz_localize`를 두 번 호출하면 오류가 난다 — `bms_raw.csv`는 이미 `+09:00` 오프셋이 포함돼 있으므로 `tz_localize` 없이 바로 `tz_convert`만 한다(`standardize.py`에 이미 반영)
- 원본 파일이 없다는 오류가 나면 `ch01_setup/generate_sample_data.py`를 먼저 실행했는지 확인한다
