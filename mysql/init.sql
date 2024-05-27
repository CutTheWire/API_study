GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '760329' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SET NAMES 'utf8mb4';

CREATE DATABASE IF NOT EXISTS TEST_DB;

SHOW WARNINGS;

USE TEST_DB;

CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE youtube (
    video_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    channel_title VARCHAR(255) NOT NULL,
    view_count BIGINT NOT NULL,
    like_count BIGINT,
    comment_count BIGINT
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE youtube_music (
    video_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    channel_title VARCHAR(255) NOT NULL,
    view_count BIGINT NOT NULL,
    like_count BIGINT,
    comment_count BIGINT
) ENGINE=InnoDB CHARSET=utf8mb4;

INSERT INTO users (id, name, email, created_at) VALUES
('gain', '한가인', 'gain@example.com', '2024-05-10 07:40:00'),
('younghi', '이영희', 'younghi@example.com', '2024-05-10 09:00:00'),
('junyoung', '박준영', 'junyoung@example.com', '2024-05-10 11:00:00'),
('hyunjung', '최현정', 'hyunjung@example.com', '2024-05-10 12:20:00'),
('chulsoo', '김철수', 'chulsoo@example.com', '2024-05-10 16:20:00'),
('doyoun', '이도윤', 'doyoun@example.com', '2024-05-10 16:30:00'),
('seojoon', '박서준', 'seojoon@example.com', '2024-05-10 16:40:00'),
('minsoo', '정민수', 'minsoo@example.com', '2024-05-10 18:40:00'),
('yuri', '최유리', 'yuri@example.com', '2024-05-10 21:30:00'),
('jia', '김지아', 'jia@example.com', '2024-05-10 22:00:00');


