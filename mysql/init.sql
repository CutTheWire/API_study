GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '760329' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SET NAMES 'utf8mb4';

CREATE DATABASE IF NOT EXISTS test_db;

-- 데이터베이스 사용
USE test_db;
SHOW WARNINGS;

CREATE TABLE user_tb (
  user_idx INT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255),
  pw VARCHAR(255),
  user_name VARCHAR(255) NOT NULL,
  phone_number VARCHAR(255),
  gender INT DEFAULT 0,
  provider VARCHAR(255) DEFAULT 'local',
  sns_id VARCHAR(255),
  device_token VARCHAR(255),
  created_at DATETIME DEFAULT NOW(),
  expired_at DATETIME DEFAULT NULL,
  updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),
  UNIQUE(user_id)
);

CREATE TABLE iot_tb (
  iot_idx INT AUTO_INCREMENT PRIMARY KEY,
  iot_id VARCHAR(255) UNIQUE NOT NULL,
  user_idx INT UNIQUE,
  iot_name VARCHAR(255),
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),
  FOREIGN KEY (user_idx) REFERENCES user_tb(user_idx)
);

CREATE TABLE subscribe_tb (
  subscribe_idx INT AUTO_INCREMENT PRIMARY KEY,
  user_idx INT,
  created_at DATETIME DEFAULT NOW(),
  expired_at DATETIME DEFAULT NULL,
  updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),
  FOREIGN KEY (user_idx) REFERENCES user_tb(user_idx)
);

CREATE TABLE inquiry_tb (
  inquiry_idx INT AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(255) NOT NULL,
  phone_number VARCHAR(255) NOT NULL,
  contents VARCHAR(255) NOT NULL,
  user_idx INT,
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),
  FOREIGN KEY (user_idx) REFERENCES user_tb(user_idx)
);

CREATE TABLE iot_log_tb (
  id INT AUTO_INCREMENT PRIMARY KEY,
  iot_id VARCHAR(255) NOT NULL,
  log TEXT NOT NULL,
  timestamp DATETIME NOT NULL,
  FOREIGN KEY (iot_id) REFERENCES iot_tb(iot_id)
);

CREATE TABLE iot_sensor_tb (
  id INT AUTO_INCREMENT PRIMARY KEY,
  iot_id VARCHAR(255) NOT NULL,
  measured_weight INT NOT NULL,
  timestamp DATETIME NOT NULL,
  status BOOLEAN NOT NULL,
  FOREIGN KEY (iot_id) REFERENCES iot_tb(iot_id)
);

CREATE EVENT IF NOT EXISTS clear_expired_tokens
ON SCHEDULE EVERY 1 MINUTE
DO
  UPDATE user_tb
  SET device_token = NULL,
      expired_at = NULL
  WHERE expired_at < NOW();

  -- 이벤트 스케줄러 활성화
SET GLOBAL event_scheduler = 1;


-- -- user_tb에 데이터 삽입
-- INSERT INTO user_tb (user_id, pw, user_name, phone_number, gender, provider, sns_id, device_token) VALUES
-- ('user1', 'pw1', 'Alice', '123-456-7890', 0, 'local', NULL, 'token1'),
-- ('user2', 'pw2', 'Bob', '234-567-8901', 1, 'local', NULL, 'token2'),
-- ('user3', 'pw3', 'Charlie', '345-678-9012', 1, 'local', NULL, 'token3');

-- -- iot_tb에 데이터 삽입
-- INSERT INTO iot_tb (iot_id, user_idx, iot_name) VALUES
-- ('iot1', 1, 'IoT Device 1'),
-- ('iot2', 2, 'IoT Device 2'),
-- ('iot3', 3, 'IoT Device 3');

-- -- subscribe_tb에 데이터 삽입
-- INSERT INTO subscribe_tb (user_idx) VALUES
-- (1),
-- (2),
-- (3);

-- -- inquiry_tb에 데이터 삽입
-- INSERT INTO inquiry_tb (type, phone_number, contents, user_idx) VALUES
-- ('Type1', '123-456-7890', 'Inquiry 1', 1),
-- ('Type2', '234-567-8901', 'Inquiry 2', 2),
-- ('Type3', '345-678-9012', 'Inquiry 3', 3);

-- -- iot_log_tb에 데이터 삽입
-- INSERT INTO iot_log_tb (iot_id, log, timestamp) VALUES
-- ('iot1', 'Log entry 1 for IoT 1', NOW()),
-- ('iot2', 'Log entry 2 for IoT 2', NOW()),
-- ('iot3', 'Log entry 3 for IoT 3', NOW());

-- -- iot_sensor_tb에 데이터 삽입
-- INSERT INTO iot_sensor_tb (iot_id, measured_weight, timestamp, status) VALUES
-- ('iot1', 100, NOW(), TRUE),
-- ('iot2', 150, NOW(), FALSE),
-- ('iot3', 200, NOW(), TRUE);
