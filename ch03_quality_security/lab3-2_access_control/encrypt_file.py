"""외부(협력사 등)로 내보내는 CSV 파일 자체를 암호화한다. DB 내부 컬럼 암호화(pgcrypto)와는
별개로, 파일 단위로 전달할 때 쓰는 애플리케이션 레벨 암호화 예시."""
from pathlib import Path

from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[2]
IN_PATH = ROOT / "data" / "processed" / "quality_checked.csv"
OUT_PATH = ROOT / "data" / "processed" / "quality_checked.csv.enc"
KEY_PATH = Path(__file__).resolve().parent / "secret.key"


def main():
    if KEY_PATH.exists():
        key = KEY_PATH.read_bytes()
    else:
        key = Fernet.generate_key()
        KEY_PATH.write_bytes(key)
        print(f"generated new key: {KEY_PATH} (실습용 — 실제로는 별도 키 관리 방식 사용)")

    f = Fernet(key)
    encrypted = f.encrypt(IN_PATH.read_bytes())
    OUT_PATH.write_bytes(encrypted)
    print(f"saved: {OUT_PATH}")

    # 복호화 확인
    decrypted = f.decrypt(OUT_PATH.read_bytes())
    assert decrypted == IN_PATH.read_bytes()
    print("decrypt check: OK")


if __name__ == "__main__":
    main()
