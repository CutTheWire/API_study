import mysql.connector
from dotenv import load_dotenv
from datetime import datetime 
import os
from utils.auth import hash_password

# 환경 변수 로드
load_dotenv()

# 데이터베이스 설정
db_config = {
    'host': "mysql",
    'user': os.getenv('MYSQL_ROOT_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': 3306
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
            "INSERT INTO user_tb (user_id, pw, user_name, phone_number) "
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
        query = "SELECT * FROM user_tb WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user
    
    except mysql.connector.Error as err:
        print(f"데이터베이스 오류: {err}")
        raise
    
    finally:
        cursor.close()
        conn.close()
        
def update_user_token(user_id: str, token: str, expires_at: datetime):
    """
    사용자 토큰과 만료 시간을 업데이트하는 함수
    :param user_id: 사용자 ID
    :param token: 생성된 토큰
    :param expires_at: 토큰 만료 시간
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        update_token_query = (
            "UPDATE user_tb SET device_token = %s, expires_at = %s WHERE user_id = %s"
        )
        cursor.execute(update_token_query, (token, expires_at, user_id))
        conn.commit()
    
    except mysql.connector.Error as err:
        print(f"데이터베이스 오류: {err}")
        conn.rollback()
        raise
    
    finally:
        cursor.close()
        conn.close()


# 일별 기기 정보
def get_day_all_cursor(self, iotId):
    today = datetime.now().date()
    cursor = self.local_conn.cursor()
    query = """
        SELECT * FROM iot_sensor_tb 
        WHERE iot_id = %s AND DATE(created_at) = %s
    """
    cursor.execute(query, (iotId, today,))
    result = cursor.fetchall()
    cursor.close()
    return result

# 월별 기기 정보
def get_month_all_cursor(self, iotId):
    today = datetime.now().date()
    current_month = today.strftime('%Y-%m')
    cursor = self.local_conn.cursor()
    query = """
        SELECT * FROM iot_sensor_tb 
        WHERE iot_id = %s AND DATE_FORMAT(created_at, '%%Y-%%m') = %s
    """
    cursor.execute(query, (iotId, current_month,))
    result = cursor.fetchall()
    cursor.close()
    return result
