import mysql.connector
from dotenv import load_dotenv
import os
from utils.auth import hash_password

# 환경 변수 로드
load_dotenv()

# 데이터베이스 설정
db_config = {
    'host': "localhost",
    'user': os.getenv('MYSQL_ROOT_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': int(3310)
}

# 데이터베이스 연결 풀 생성
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def get_connection():
    """
    데이터베이스 연결을 얻는 함수
    :return: mysql.connector 연결 객체
    """
    return connection_pool.get_connection()

def create_user(user):
    """
    사용자를 생성하는 함수
    :param user: 사용자 생성 스키마
    :return: 생성된 사용자 ID
    """
    hashed_password = hash_password(user.pw)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        add_user_query = (
            "INSERT INTO users (user_id, pw, user_name, phone_number) "
            "VALUES (%s, %s, %s, %s)"
        )
        user_data = (
            user.user_id,
            hashed_password,
            user.user_name,
            user.phone_number
        )
        cursor.execute(add_user_query, user_data)
        conn.commit()
        return cursor.lastrowid  # 생성된 사용자 ID 반환
    except mysql.connector.Error as err:
        print(f"데이터베이스 오류: {err}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(user_id: str):
    """
    사용자 ID로 사용자를 조회하는 함수
    :param user_id: 사용자 ID
    :return: 사용자 정보 (dict)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"데이터베이스 오류: {err}")
        raise
    finally:
        cursor.close()
        conn.close()
