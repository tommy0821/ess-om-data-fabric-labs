# 5장. 종합 미니 프로젝트

> 책 5장 참고 · ch02~ch04의 Lab 결과물을 이어 붙여 site_A의 이상 징후를 탐지하고 리포트를 생성하는 엔드투엔드 미니 프로젝트

## 목표
- 2~4장에서 만든 Lab 산출물을 하나의 파이프라인으로 잇는다
- 책 전체가 다룬 데이터 패브릭 아키텍처(수집→통합→품질/보안→활용)를 실습으로 완성한다

## Lab 산출물 체인

| 단계 | Lab | 산출물 |
|---|---|---|
| 수집 | 2-1 | (실시간 스트림, 파일로는 저장하지 않음) |
| 표준화 | 2-2 | `data/processed/unified_long.csv` |
| 자동화 | 2-3 | Kafka 토픽 + Airflow DAG |
| 품질 정제 | 3-1 | `data/processed/quality_checked.csv` |
| 접근제어·암호화 | 3-2 | Postgres RLS 테이블, `quality_checked.csv.enc` |
| 시계열 예측 | 4-1 | `data/processed/temp_forecast.csv` |
| 이상탐지 | 4-2 | `data/processed/anomaly_flags.csv` |
| 패브릭 연계 | 4-3 | `data/processed/unified_long_with_ai.csv` |

## 준비물
- ch01_setup ~ ch04_ai_analysis의 산출물 (직접 순서대로 실행했거나, 아래 `run_pipeline.py`로 한 번에 실행)

## 단계별 절차

**옵션 A — 파일 기반 단계만 한 번에 실행** (Docker가 필요한 2-3, 3-2는 제외)
```bash
python ch05_capstone/run_pipeline.py
```
`ch01_setup`(데이터 생성) → `lab2-2`(표준화) → `lab3-1`(이상치 주입·정제) → `lab4-1~4-3`(예측·이상탐지·패브릭 연계) 순서로 실행되어 최종적으로 `data/processed/unified_long_with_ai.csv`를 만든다.

**옵션 B — 전체 체인을 각 장의 README를 따라 하나씩 직접 실행** (Lab 2-1, 2-3, 3-2 포함)

## 미니 프로젝트 과제 (자율 실습)
`run_pipeline.py`가 만든 `unified_long_with_ai.csv`를 입력으로, 다음을 수행하는 "site_A 일일 리포트" 로직을 직접 이어서 작성해본다.

1. `metric == "anomaly_score"`인 행에서 스코어가 임계값을 넘는 시점을 찾는다
2. 그 시점 전후의 `temp_c`, `temp_c_forecast`, `volt`, `curr` 값을 함께 뽑아 원인을 짐작할 단서를 만든다
3. "PCS-01, 08:00~08:30 구간 이상 징후 감지"처럼 사람이 읽을 수 있는 요약 문구를 만든다

리포트 형식(마크다운 파일, 이메일, Slack 메시지 등)과 임계값은 정해두지 않았다 — 정답이 있는 실습이 아니라, 지금까지 배운 Lab들을 스스로 조합해보는 과제로 남겨둔다. 2장 Lab 2-3에서 만든 Airflow DAG(`standardize_ess_data`)을 확장해서, 이 리포트 로직을 매일 자동 실행되게 만들어보는 것도 좋은 다음 단계다.

## 결과 확인
- `data/processed/unified_long_with_ai.csv`에 원본 센서 지표(`volt`, `curr`, `temp_c`, `soc_pct`, `cell_temp_max`)와 AI 분석 지표(`temp_c_forecast`, `anomaly_score`)가 함께 들어있는지 확인한다
