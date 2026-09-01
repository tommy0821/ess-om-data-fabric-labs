"""Modbus 수집기(클라이언트). modbus_pcs_simulator.py를 먼저 띄운 뒤 실행한다."""
import csv
import time
from pathlib import Path

from pymodbus.client import ModbusTcpClient

LOG_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "ingest_log.csv"


def append_log(rows: list[dict]) -> None:
    """공통 롱 포맷(ts, device, metric, value)으로 기록 — collect_mqtt.py와 같은 파일에 섞여도 컬럼이 어긋나지 않는다."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    is_new = not LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ts", "device", "metric", "value"])
        if is_new:
            writer.writeheader()
        writer.writerows(rows)


def main():
    client = ModbusTcpClient("localhost", port=5020)
    client.connect()

    while True:
        result = client.read_holding_registers(0, 3)
        volt, curr, temp = result.registers
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        rows = [
            {"ts": ts, "device": "PCS-01", "metric": "volt", "value": volt / 10},
            {"ts": ts, "device": "PCS-01", "metric": "curr", "value": curr},
            {"ts": ts, "device": "PCS-01", "metric": "temp_c", "value": temp / 10},
        ]
        print(rows)
        append_log(rows)
        time.sleep(5)


if __name__ == "__main__":
    main()
