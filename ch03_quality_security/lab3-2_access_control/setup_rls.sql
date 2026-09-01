-- 역할 2개 생성: site_operator(전체 조회), partner_viewer(민감하지 않은 지표만 조회)
CREATE ROLE site_operator LOGIN PASSWORD 'op_pass';
CREATE ROLE partner_viewer LOGIN PASSWORD 'partner_pass';
GRANT SELECT ON ess_readings TO site_operator, partner_viewer;

-- Row-Level Security 활성화
ALTER TABLE ess_readings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ess_readings FORCE ROW LEVEL SECURITY;  -- 테이블 소유자에게도 정책 적용

CREATE POLICY operator_full_access ON ess_readings
  FOR SELECT TO site_operator
  USING (true);

-- volt, curr처럼 사업장 출력 성능과 직결되는 지표는 제외하고 soc_pct, temp_c만 공개
CREATE POLICY partner_limited_access ON ess_readings
  FOR SELECT TO partner_viewer
  USING (metric IN ('soc_pct', 'temp_c'));

-- 컬럼 암호화(pgcrypto) — device_id처럼 민감한 식별자를 DB 안에서 암호화해 저장
CREATE EXTENSION IF NOT EXISTS pgcrypto;

ALTER TABLE ess_readings ADD COLUMN IF NOT EXISTS device_id_enc bytea;
UPDATE ess_readings SET device_id_enc = pgp_sym_encrypt(device_id, 'enc_key_here');
-- 조회 시: SELECT pgp_sym_decrypt(device_id_enc, 'enc_key_here') FROM ess_readings;
