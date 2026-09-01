"""BMS 역할로 MQTT에 값을 발행(publish)한다. 공개 테스트 브로커(test.mosquitto.org)를 사용한다."""
import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "ess/site_A/bms01"


def main():
    client = mqtt.Client()
    client.connect(BROKER, 1883)

    while True:
        payload = {"unit_id": "BMS-01", "soc_pct": round(random.uniform(20, 90), 1)}
        client.publish(TOPIC, json.dumps(payload))
        print("published:", payload)
        time.sleep(5)


if __name__ == "__main__":
    main()
