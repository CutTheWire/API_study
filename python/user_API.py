from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from threading import local
from googleapiclient.discovery import build
from dotenv import load_dotenv
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
api_key = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

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

class Queries:
    def __init__(self):
        self._local_conn = None

    @property
    def local_conn(self):
        if self._local_conn is None or not self._local_conn.is_connected():
            self._local_conn = mysql.connector.connect(**db_config)
        return self._local_conn

    def create_user_cursor(self, user_id, name, email):
        now = datetime.now()
        cursor = self.local_conn.cursor()
        cursor.execute("INSERT INTO users (id, name, email, created_at) VALUES (%s, %s, %s, %s)", (user_id, name, email, now,))
        self.local_conn.commit()
        cursor.close()

    def read_all_user_cursor(self):
        cursor = self.local_conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        return result

    def read_user_cursor(self, user_id):
        cursor = self.local_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def update_user_cursor(self, name, email, user_id):
        cursor = self.local_conn.cursor()
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id,))
        self.local_conn.commit()
        cursor.close()

    def update_user_id_cursor(self, email, user_id):
        cursor = self.local_conn.cursor()
        cursor.execute("UPDATE users SET id = %s WHERE email = %s", (user_id, email,))
        self.local_conn.commit()
        cursor.close()

    def delete_user_cursor(self, user_id):
        cursor = self.local_conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.local_conn.commit()
        cursor.close()

db_queries = Queries()

@app.get("/")
def main():
    return {"message": "This server SQL:CRUD TEST API. If you want to test, go to the '/docs' URL or POSTMAN."}

# 사용자 생성 (POST)
@app.post("/users/create")
async def create_user(user: UserCreate):
    try:
        db_queries.create_user_cursor(user.id, user.name, user.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": user.id, "name": user.name, "email": user.email}

# 전체 사용자 목록 가져오기 (GET)
@app.get("/users/")
async def read_users():
    try:
        users = db_queries.read_all_user_cursor()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return users

# 특정 사용자 목록 가져오기 (GET)
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    try:
        user = db_queries.read_user_cursor(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

# 사용자 정보 업데이트 (PUT)
@app.put("/users/update")
async def update_user(user: UserUpdate):
    try:
        db_queries.update_user_cursor(user.name, user.email, user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": user.id, "name": user.name, "email": user.email}

# 사용자 id 정보 업데이트 (PUT)
@app.put("/users/update/id")
async def update_user_id(user: UserUpdate):
    try:
        db_queries.update_user_id_cursor(user.email, user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": user.id, "name": user.name, "email": user.email}

# 사용자 삭제 (DELETE)
@app.delete("/users/delete/")
async def delete_user(user: UserDelete):
    try:
        db_queries.delete_user_cursor(user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "User deleted successfully"}
