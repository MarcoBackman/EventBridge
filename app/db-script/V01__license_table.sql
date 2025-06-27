START TRANSACTION;

--환경별 다음중 하나 선택
--USE DEV_EVENT_BRIDGE;
--USE UAT_EVENT_BRIDGE;
--USE PROD_EVENT_BRIDGE;

CREATE TABLE IF NOT EXISTS client_download_license (
    license_id INT AUTO_INCREMENT PRIMARY KEY,
    license_key VARCHAR(200) NOT NULL UNIQUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_used_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_used BOOL NOT NULL DEFAULT FALSE,
    is_blocked BOOL NOT NULL DEFAULT FALSE,
    expiration_date TIMESTAMP NULL,
    use_counts INT NOT NULL DEFAULT 0,
    use_limit INT NOT NULL DEFAULT 10
);

ALTER TABLE client_download_license ADD COLUMN license_key_hint VARCHAR(50) NOT NULL;
ALTER TABLE client_download_license ADD COLUMN license_type VARCHAR(50) NOT NULL;

SELECT 'client_download_license table has been created successfully' AS Message;

COMMIT;