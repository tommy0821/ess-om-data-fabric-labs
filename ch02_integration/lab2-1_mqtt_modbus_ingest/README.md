# Lab 2-1. PCS·BMS 데이터 수집 파이프라인 구축 (Modbus/MQTT)

> 책 2장 2.2절 참고

## 목표
- Modbus(폴링 방식)와 MQTT(구독 방식)라는 서로 다른 통신 방식을 하나의 수집 파이프라인으로 통합한다
- Docker 없이 로컬에서 두 프로토콜을 각각 시뮬레이션하고 수집한다

## 준비물
- `pymodbus`, `paho-mqtt` (저장소 루트 `requirements.txt`에 포함됨)
- 인터넷 연결(공개 MQTT 테스트 브로커 `test.mosquitto.org` 사용)

## 파일 구성
| 파일 | 역할 |
|---|---|
| `modbus_pcs_simulator.py` | PCS 역할 — Modbus TCP 서버(레지스터에 전압/전류/온도 값 보유) |
| `collect_modbus.py` | Modbus 클라이언트 — 5초마다 폴링해서 로그에 기록 |
| `publish_bms.py` | BMS 역할 — MQTT로 SOC 값을 5초마다 발행 |
| `collect_mqtt.py` | MQTT 구독자 — 발행된 값을 받아 로그에 기록 |

## 단계별 절차
1. 터미널 4개를 열고 순서대로 실행한다.
   ```bash
   # 터미널 1
   python modbus_pcs_simulator.py

   # 터미널 2
   python collect_modbus.py

   # 터미널 3
   python collect_mqtt.py

   # 터미널 4
   python publish_bms.py
   ```
2. `collect_modbus.py`, `collect_mqtt.py` 두 수집기 모두 저장소 루트의 `data/processed/ingest_log.csv`에 **공통 롱 포맷**(`ts, device, metric, value`)으로 append한다 — 프로토콜은 다르지만 저장 스키마를 통일해서 한 파일에 섞여도 깨지지 않게 했다.

## 결과 확인
- `collect_modbus.py` 터미널에 5초 간격으로 `{"ts": ..., "device": "PCS-01", "metric": "volt", ...}` 형태의 로그가 여러 줄(volt/curr/temp_c) 출력된다
- `collect_mqtt.py` 터미널에 `publish_bms.py`가 보낸 SOC 값이 그대로 찍힌다
- `data/processed/ingest_log.csv`를 열어 `device` 컬럼에 `PCS-01`과 `BMS-01`이 함께 있는지 확인한다

## 트러블슈팅
- `test.mosquitto.org` 접속이 막혀 있다면(사내망 방화벽 등): 로컬 MQTT 브로커(`mosquitto` 패키지)를 설치하거나 Lab 3-2처럼 Docker 기반 브로커로 대체한다
- Modbus 포트(5020)가 이미 사용 중이면 `modbus_pcs_simulator.py`와 `collect_modbus.py` 양쪽의 포트 번호를 함께 바꾼다
