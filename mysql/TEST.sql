GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '1234' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SET NAMES 'utf8mb4';

CREATE DATABASE TEST_DB;

SHOW WARNINGS;

USE TEST_DB;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4;

INSERT INTO users (name, email) VALUES 
('김철수', 'chulsoo@example.com'),
('이영희', 'younghi@example.com'),
('박준영', 'junyoung@example.com'),
('최현정', 'hyunjung@example.com'),
('정민수', 'minsoo@example.com'),
('한가인', 'gain@example.com'),
('김지아', 'jia@example.com'),
('이도윤', 'doyoun@example.com'),
('박서준', 'seojoon@example.com'),
('최유리', 'yuri@example.com');
