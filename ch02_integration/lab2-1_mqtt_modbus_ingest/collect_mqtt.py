"""MQTT 수집기(구독자). publish_bms.py를 먼저(또는 동시에) 실행해야 메시지가 도착한다."""
import csv
import json
import time
from pathlib import Path

import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "ess/site_A/#"
LOG_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "ingest_log.csv"


def append_log(row: dict) -> None:
    """공통 롱 포맷(ts, device, metric, value)으로 기록 — collect_modbus.py와 같은 파일에 섞여도 컬럼이 어긋나지 않는다."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    is_new = not LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ts", "device", "metric", "value"])
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    row = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": data["unit_id"],
        "metric": "soc_pct",
        "value": data["soc_pct"],
    }
    print(row)
    append_log(row)


def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883)
    client.subscribe(TOPIC)
    client.loop_forever()


if __name__ == "__main__":
    main()
