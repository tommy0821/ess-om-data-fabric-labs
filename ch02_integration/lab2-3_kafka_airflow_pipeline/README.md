# Lab 2-3. Kafka/Airflow 기반 통합 파이프라인 구성 및 동작 확인

> 책 2장 2.4절 참고 · Docker 필요 · Airflow 3.3.1 기준

## 목표
- Lab 2-1(수집)과 Lab 2-2(표준화)를 사람이 수동으로 실행하는 대신, Kafka로 흘려보내고 Airflow로 주기 실행되는 파이프라인으로 만든다

## 준비물
- Docker Desktop
- 이 폴더의 `docker-compose.yml`

## 파일 구성
| 파일 | 역할 |
|---|---|
| `docker-compose.yml` | Kafka, Zookeeper, Postgres(Airflow 메타DB), Airflow 3.3.1(apiserver/scheduler/dag-processor) |
| `producer.py` | Lab 2-1 수집 로직을 Kafka 프로듀서로 바꾼 버전 |
| `dags/standardize_ess_data.py` | Lab 2-2 표준화 로직을 담은 Airflow DAG (10분마다 실행) |

## 단계별 절차
1. 이 폴더에서 컨테이너를 띄운다.
   ```bash
   cd ch02_integration/lab2-3_kafka_airflow_pipeline
   docker compose up -d
   ```
2. Kafka 프로듀서를 실행해 `ess.raw` 토픽으로 값을 흘려보낸다.
   ```bash
   python producer.py
   ```
3. Airflow 웹 UI(`http://localhost:8080`, 최초 계정은 `airflow db migrate` 로그 또는 `docker compose logs airflow-init`에서 확인)에서 `standardize_ess_data` DAG을 활성화(Unpause)한다.

### Airflow 2 → 3 변경점
2.x의 `webserver` 단일 컨테이너가 3.x에서는 `airflow-apiserver`(UI+API)로 이름이 바뀌었고, DAG 파일을 읽어 파싱하는 역할이 스케줄러에서 분리되어 `airflow-dag-processor`라는 별도 컨테이너로 실행된다. DAG 코드(`schedule=`, `PythonOperator` import 경로)는 2.x 후반 문법과 동일해서 그대로 쓸 수 있다.

## 결과 확인
- `docker exec -it <kafka 컨테이너> kafka-console-consumer --bootstrap-server localhost:9092 --topic ess.raw`로 `producer.py`가 보낸 메시지가 도착하는지 확인
- Airflow 웹 UI에서 `standardize_ess_data` DAG이 10분마다 성공(success)으로 표시되는지, 저장소 루트의 `data/processed/unified_long.csv`가 갱신되는지 확인

## 트러블슈팅
- Airflow 컨테이너가 DAG을 못 찾으면 `docker-compose.yml`의 `./dags` 볼륨 마운트 경로가 이 폴더 기준인지 확인
- `pandas` import 오류가 나면 `airflow-init`/`airflow-scheduler`가 `_PIP_ADDITIONAL_REQUIREMENTS`로 설치를 마칠 때까지 기다린다(최초 기동 시 다소 시간이 걸린다) — 운영 환경에서는 이 방식 대신 커스텀 이미지를 미리 빌드해서 쓴다
- Kafka 브로커 접속이 안 되면 `KAFKA_ADVERTISED_LISTENERS`가 호스트에서 접근 가능한 주소로 설정됐는지 확인
