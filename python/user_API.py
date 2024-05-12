from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from threading import local
import uvicorn
import os
from datetime import datetime

app = FastAPI()
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path)

local_conn = local()

# 데이터베이스 연결 설정
db_config  = {
    'host': os.getenv('MYSQL_ROOT_HOST'),
    'user': os.getenv('MYSQL_ROOT_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': os.getenv('MYSQL_DB_PORT') 
}

# 데이터베이스 연결을 관리하는 함수
def get_db_connection():
    if not hasattr(local_conn, "conn"):
        local_conn.conn = mysql.connector.connect(**db_config)
    return local_conn.conn

# Pydantic 모델
class UserCreate(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime

class UserUpdate(BaseModel):
    id: str
    name: str
    email: str

class UserDelete(BaseModel):
    id: str

def create_user_cursor(cursor, user_id, name, email):
    now = datetime.now()
    cursor.execute("INSERT INTO users (id, name, email, created_at) VALUES (%s, %s, %s, %s)", (user_id, name, email, now,))

def read_all_user_cursor(cursor):
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

def read_user_cursor(cursor, user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchall()

def update_user_cursor(cursor, name, email, user_id):
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id,))

def update_user_id_cursor(cursor, email, user_id):
    cursor.execute("UPDATE users SET id = %s WHERE email = %s", (user_id, email,))

def delete_user_cursor(cursor, user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

@app.get("/")
def main():
    return {"message":
    "This server SQL:CRUD TEST API. If you want to test, go to the '/docs' URL or POSTMAN." }

# 사용자 생성 (POST)
@app.post("/users/create")
def create_user(user: UserCreate):
    cursor = None
    try:
        cursor = get_db_connection().cursor()
        create_user_cursor(cursor, user.id, user.name, user.email)
        get_db_connection().commit()
    except Error as e:
        get_db_connection().rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
    return {"id": user.id, "name": user.name, "email": user.email}

# 전체 사용자 목록 가져오기 (GET)
@app.get("/users/")
def read_users():
    users = []
    cursor = None
    try:
        cursor = get_db_connection().cursor()
        users = read_all_user_cursor(cursor)
    except Error as e:
        get_db_connection().rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
    return users

# 사용자 목록 가져오기 (GET)
@app.get("/users/{user_id}")
def read_users(user_id: str):
    users = []
    cursor = None
    try:
        cursor = get_db_connection().cursor()
        users = read_user_cursor(cursor, user_id)
        if cursor.rowcount == 0:
            get_db_connection().rollback()
            raise HTTPException(status_code=404, detail="User not found")
    except Error as e:
        get_db_connection().rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
    return users

# 사용자 정보 업데이트 (PUT)
@app.put("/users/update")
def update_user(user: UserUpdate):
    cursor = None
    try:
        cursor = get_db_connection().cursor()
        update_user_cursor(cursor, user.name, user.email, user.id)
        get_db_connection().commit()
        if cursor.rowcount == 0:
            get_db_connection().rollback()
            raise HTTPException(status_code=404, detail="User not found")
    except Error as e:
        get_db_connection().rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
    return {"id": user.id, "name": user.name, "email": user.email}

# 사용자 id 정보 업데이트 (PUT)
@app.put("/users/update/id")
def update_user(user: UserUpdate):
    cursor = None
    try:
        cursor = get_db_connection().cursor()
        update_user_id_cursor(cursor, user.email, user.id)
        get_db_connection().commit()
        if cursor.rowcount == 0:
            get_db_connection().rollback()
            raise HTTPException(status_code=404, detail="User not found")
    except Error as e:
        get_db_connection().rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
    return {"id": user.id, "name": user.name, "email": user.email}

# 사용자 삭제 (DELETE)
@app.delete("/users/delete/")
def delete_user(user: UserDelete):
    cursor = None
    try:
        cursor = get_db_connection().cursor()
        delete_user_cursor(cursor, user.id)
        get_db_connection().commit()
        if cursor.rowcount == 0:
            get_db_connection().rollback()  # 변경사항이 반영되지 않도록 롤백
            raise HTTPException(status_code=404, detail="User not found")
    except Error as e:
        get_db_connection().rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
    return {"message": "User deleted successfully"}
