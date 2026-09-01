# ess-om-data-fabric-labs

교재 **"ESS O&M 데이터 패브릭 구성" (ESS O&M Data Fabric: Design and Implementation)**의 실습(Lab) 코드·데이터 저장소입니다. 원고 자체는 별도 관리하며, 이 저장소는 책의 각 장에 나오는 Lab을 실제로 따라 할 수 있는 코드/데이터만 모아둡니다.

## 프로젝트 구조

```
ess-om-data-fabric-labs/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                        # 원본 샘플 데이터 (ch01_setup에서 생성)
│   │   ├── pcs_raw.csv
│   │   └── bms_raw.csv
│   └── processed/                  # Lab에서 정제·가공한 산출물 (전부 재생성 가능, git 추적 안 함)
│
├── ch01_setup/                     # 1장: 실습 환경 준비
│   └── generate_sample_data.py     # site_A(PCS/BMS) 가상 데이터 생성기
│
├── ch02_integration/                # 2장: 분산 데이터소스 통합
│   ├── lab2-1_mqtt_modbus_ingest/       # Modbus(PCS)·MQTT(BMS) 수집
│   ├── lab2-2_schema_standardization/   # 표준 스키마 통합 + 메타데이터 카탈로그
│   └── lab2-3_kafka_airflow_pipeline/   # Kafka + Airflow 3.3.1 자동화 (Docker)
│
├── ch03_quality_security/           # 3장: 데이터 품질 및 보안
│   ├── lab3-1_outlier_detection/        # IQR + IsolationForest 이상치 탐지·정제
│   └── lab3-2_access_control/           # Postgres RLS 접근제어 + 암호화 (Docker)
│
├── ch04_ai_analysis/                # 4장: AI 기반 데이터 처리 및 분석
│   ├── lab4-1_timeseries_forecast/      # Keras LSTM 온도 예측
│   ├── lab4-2_anomaly_detection/        # 잔차 기반 이상탐지
│   └── lab4-3_fabric_integration/       # 분석 결과를 표준 스키마로 재연계
│
└── ch05_capstone/                   # 5장: 종합 미니 프로젝트
    └── run_pipeline.py                  # 파일 기반 단계(2-2,3-1,4-1~4-3) 일괄 실행 스타터
```

`ch0N_` 접두사는 정렬 순서를 위한 것이고, 각 `labN-M_.../` 폴더 안에는 책의 Lab 표준 포맷(목표 → 준비물 → 단계별 절차 → 결과 확인 → 트러블슈팅)을 따르는 `README.md`가 있습니다. Docker가 필요한 Lab(2-3, 3-2)은 폴더 안에 `docker-compose.yml`이 함께 있습니다.

## 라이브러리 설치

```bash
# 1. 가상환경 생성
python3 -m venv .venv

# 2. 가상환경 활성화
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt`에는 장별로 필요한 패키지가 주석으로 구분되어 있습니다.

| 구분 | 패키지 | 용도 |
|---|---|---|
| 공통 | pandas, numpy, matplotlib, jupyterlab | 데이터 처리·시각화·노트북 |
| 2장 | paho-mqtt, pymodbus | Lab 2-1: MQTT/Modbus 시뮬레이터 |
| 2장 | kafka-python | Lab 2-3: Kafka 프로듀서/컨슈머 |
| 3장 | scikit-learn | Lab 3-1: 이상치 탐지, Lab 4-2에도 재사용 |
| 3장 | cryptography | Lab 3-2: 파일 암호화(Fernet) |
| 3장 | sqlalchemy, psycopg2-binary | Lab 3-2: Postgres 적재 |
| 4장 | tensorflow | Lab 4-1: 시계열 예측(Keras LSTM) |

> **Apache Airflow(Lab 2-3)**는 `requirements.txt`에 포함하지 않았습니다. Python 버전별 constraints 파일이 필요해 pip로 바로 설치하면 의존성 충돌이 잦으므로, `ch02_integration/lab2-3_kafka_airflow_pipeline/docker-compose.yml`로 띄우는 방식을 사용합니다.

## 샘플 데이터 생성

`data/raw/`의 `pcs_raw.csv`, `bms_raw.csv`는 아래 스크립트로 생성한 것입니다. 필요하면 재실행해서 다시 만들 수 있습니다.

```bash
cd ch01_setup
python generate_sample_data.py
```

- `pcs_raw.csv` — 컬럼: `ts, device, volt, curr, temp_c, status_code`
- `bms_raw.csv` — 컬럼: `timestamp, unit_id, soc_pct, cell_temp_max`

PCS와 BMS의 컬럼명·타임스탬프 포맷이 의도적으로 다릅니다 — 실제 현장에서 겪는 이기종 데이터 문제를 재현한 것이며, 이 차이를 표준 스키마로 맞추는 것이 `ch02_integration/lab2-2_schema_standardization`의 목표입니다.

## 전체 Lab 실행 순서

각 Lab 폴더의 README를 따라 순서대로 실행하면 되고, Docker가 필요 없는 단계(2-2, 3-1, 4-1~4-3)는 `ch05_capstone/run_pipeline.py`로 한 번에 실행할 수도 있습니다.

```bash
python ch05_capstone/run_pipeline.py
```

| 순서 | Lab | 실행 위치 | 산출물 |
|---|---|---|---|
| 1 | 1장 데이터 생성 | `ch01_setup/` | `data/raw/pcs_raw.csv`, `bms_raw.csv` |
| 2 | Lab 2-1 | `ch02_integration/lab2-1_mqtt_modbus_ingest/` | `data/processed/ingest_log.csv` |
| 3 | Lab 2-2 | `ch02_integration/lab2-2_schema_standardization/` | `data/processed/unified_long.csv` |
| 4 | Lab 2-3 (Docker) | `ch02_integration/lab2-3_kafka_airflow_pipeline/` | Kafka 토픽, Airflow DAG |
| 5 | Lab 3-1 | `ch03_quality_security/lab3-1_outlier_detection/` | `data/processed/quality_checked.csv` |
| 6 | Lab 3-2 (Docker) | `ch03_quality_security/lab3-2_access_control/` | Postgres RLS 테이블, `quality_checked.csv.enc` |
| 7 | Lab 4-1 | `ch04_ai_analysis/lab4-1_timeseries_forecast/` | `data/processed/temp_forecast.csv` |
| 8 | Lab 4-2 | `ch04_ai_analysis/lab4-2_anomaly_detection/` | `data/processed/anomaly_flags.csv` |
| 9 | Lab 4-3 | `ch04_ai_analysis/lab4-3_fabric_integration/` | `data/processed/unified_long_with_ai.csv` |
| 10 | 5장 미니 프로젝트 | `ch05_capstone/` | 자율 과제(리포트 로직) |
