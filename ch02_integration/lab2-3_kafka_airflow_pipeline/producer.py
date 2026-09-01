"""Lab 2-1의 수집 로직을 Kafka 프로듀서로 바꾼 버전. docker-compose가 떠 있어야 한다."""
import json
import time

from kafka import KafkaProducer

TOPIC = "ess.raw"


def main():
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode(),
    )
    while True:
        message = {"device": "PCS-01", "volt": 380.2, "curr": 12.1, "temp_c": 28.4}
        producer.send(TOPIC, message)
        print("sent:", message)
        time.sleep(5)


if __name__ == "__main__":
    main()
