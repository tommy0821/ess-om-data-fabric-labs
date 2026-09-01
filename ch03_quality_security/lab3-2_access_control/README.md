# Lab 3-2. 접근제어·암호화 설정 실습

> 책 3장 3.3절 참고 · Docker 필요

## 목표
- PostgreSQL의 Row-Level Security(RLS)로 역할별 조회 범위를 다르게 설정한다
- 저장 데이터를 암호화하는 두 가지 방식(DB 컬럼 암호화, 파일 암호화)을 실습한다

## 준비물
- Docker Desktop
- `sqlalchemy`, `psycopg2-binary`, `cryptography` (저장소 루트 `requirements.txt`에 포함됨)
- Lab 3-1의 산출물 `data/processed/quality_checked.csv`

## 파일 구성
| 파일 | 역할 |
|---|---|
| `docker-compose.yml` | Postgres 16 (포트 5432) |
| `load_to_db.py` | `quality_checked.csv`를 `ess_readings` 테이블로 적재 |
| `setup_rls.sql` | 역할 생성, RLS 정책, pgcrypto 컬럼 암호화 |
| `encrypt_file.py` | CSV 파일 자체를 Fernet으로 암호화(외부 반출용) |

> 2장 Lab 2-3에서도 Postgres를 쓴다 — 두 컨테이너를 동시에 띄우면 5432 포트가 충돌하니, 이 Lab을 실습할 때는 2-3의 `docker compose`를 먼저 내려두는 것을 권장한다(`docker compose down`).

## 단계별 절차
1. Postgres 컨테이너를 띄운다.
   ```bash
   cd ch03_quality_security/lab3-2_access_control
   docker compose up -d
   ```
2. 데이터를 적재한다.
   ```bash
   python load_to_db.py
   ```
3. 역할·RLS 정책·컬럼 암호화를 설정한다.
   ```bash
   docker compose exec -T postgres psql -U postgres -d postgres < setup_rls.sql
   ```
4. 파일 암호화를 실습한다.
   ```bash
   python encrypt_file.py
   ```

## 결과 확인
- 역할별로 접속해서 조회 범위가 다른지 확인한다.
  ```bash
  docker compose exec postgres psql -U partner_viewer -d postgres \
    -c "SELECT DISTINCT metric FROM ess_readings;"
  # -> soc_pct, temp_c 만 보여야 함

  docker compose exec postgres psql -U site_operator -d postgres \
    -c "SELECT DISTINCT metric FROM ess_readings;"
  # -> volt, curr, temp_c, soc_pct, cell_temp_max 전체가 보여야 함
  ```
- `data/processed/quality_checked.csv.enc`를 텍스트 에디터로 열었을 때 내용을 알아볼 수 없는지 확인한다 — `encrypt_file.py`가 실행 끝에 자체적으로 복호화 검증(`decrypt check: OK`)도 출력한다

## 트러블슈팅
- `FORCE ROW LEVEL SECURITY`를 빼먹으면 테이블 소유자(관리자 계정)는 정책과 무관하게 전체가 보인다 — `setup_rls.sql`에 이미 반영돼 있다
- 5432 포트 충돌 오류가 나면 2장 Lab 2-3의 `docker compose down`을 먼저 실행했는지 확인한다
- `secret.key`는 `.gitignore`에 등록돼 있다 — 실습용으로만 로컬에 두고, 실제로는 별도 키 관리 방식(예: 클라우드 KMS)을 쓴다
