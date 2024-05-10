# API_study
FastAPI, MYSQL USE &amp; STUDY 

## [qwer9679](https://github.com/qwer9679) 와 같이 진행 

## SQL 
```
CREATE DATABASE TEST_DB;

USE TEST_DB;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

```
