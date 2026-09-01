"""2~4장 Lab 스크립트를 순서대로 실행하는 시작점(starter). 리포트 생성(요약 문구, 임계값 등)은
책 5.1절에서 의도적으로 열어둔 자율 과제이므로 여기에 포함하지 않았다 — 직접 이어서 작성해보자.

Kafka/Airflow(Lab 2-3), DB 접근제어(Lab 3-2)는 Docker 컨테이너가 별도로 떠 있어야 하므로
이 스크립트에서는 파일 기반으로 진행 가능한 단계(2-2, 3-1, 4-1~4-3)만 순서대로 실행한다.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    "ch01_setup/generate_sample_data.py",
    "ch02_integration/lab2-2_schema_standardization/standardize.py",
    "ch03_quality_security/lab3-1_outlier_detection/inject_noise.py",
    "ch03_quality_security/lab3-1_outlier_detection/detect_outliers.py",
    "ch04_ai_analysis/lab4-1_timeseries_forecast/train_forecast.py",
    "ch04_ai_analysis/lab4-2_anomaly_detection/detect_anomaly.py",
    "ch04_ai_analysis/lab4-3_fabric_integration/integrate_to_fabric.py",
]


def main():
    for step in STEPS:
        script = ROOT / step
        print(f"\n=== {step} ===")
        # ch01_setup/generate_sample_data.py는 자기 폴더 기준 상대경로(../data/raw/...)를 쓰므로
        # 항상 스크립트가 있는 폴더를 cwd로 잡고 실행한다(나머지 스크립트는 cwd와 무관하게 동작).
        subprocess.run([sys.executable, str(script)], check=True, cwd=script.parent)

    print("\n완료: data/processed/unified_long_with_ai.csv 가 최종 산출물입니다.")
    print("다음: 이 파일을 읽어 이상 스코어가 임계값을 넘는 시점을 찾아 리포트로 요약하는 코드를 이어서 작성해보세요.")


if __name__ == "__main__":
    main()
