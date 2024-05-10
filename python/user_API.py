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

@app.get("/user")

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

class DB_docking:
    def __init__(self) -> None:
        self.db_config  = {
            'host': os.getenv('MYSQL_ROOT_HOST'),
            'user': os.getenv('MYSQL_ROOT_USER'),
            'password': os.getenv('MYSQL_ROOT_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'port': os.getenv('MYSQL_DB_PORT')
        }
        self.local_conn = local()

    @property
    def connection(self):
        if not hasattr(self.local_conn, "conn"):
            self.local_conn.conn = mysql.connector.connect(**self.db_config)
        return self.local_conn.conn

    def create_user_cursor(self, cursor, name, email, user_id):
        now = datetime.now()
        cursor.execute("INSERT INTO users (id, name, email, created_at) VALUES (%s, %s, %s, %s)", (user_id, name, email, now))

    def read_all_user_cursor(self, cursor):
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
    def read_user_cursor(self, cursor, user_id):
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchall()
    
    def update_user_cursor(self, cursor, name, email, user_id):
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    
    def update_user_id_cursor(self, cursor, email, user_id):
        cursor.execute("UPDATE users SET id = %s WHERE email = %s", (user_id, email))

    def delete_user_cursor(self, cursor, user_id):
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

@app.get("/")
def main():
    return {"message":
    "This server SQL:CRUD TEST API. If you want to test, go to the '/docs' URL or POSTMAN." }

# 사용자 생성 (POST)
@app.post("/users/create")
def create_user(user: UserCreate):
    conn = None
    cursor = None
    try:
        db_dk = DB_docking()
        conn = db_dk.connection
        cursor = conn.cursor()
        db_dk.create_user_cursor(cursor, user.id, user.name, user.email)
        conn.commit()
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return {"id": user.id, "name": user.name, "email": user.email}

# 전체 사용자 목록 가져오기 (GET)
@app.get("/users/")
def read_users():
    users = []
    conn = None
    cursor = None
    try:
        db_dk= DB_docking()
        conn = db_dk.connection
        cursor = conn.cursor(dictionary=True)
        users = db_dk.read_all_user_cursor(cursor)
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return users

# 사용자 목록 가져오기 (GET)
@app.get("/users/{user_id}")
def read_users(user_id: str):
    users = []
    conn = None
    cursor = None
    try:
        db_dk= DB_docking()
        conn = db_dk.connection
        cursor = conn.cursor(dictionary=True)
        users = db_dk.read_user_cursor(cursor, user_id)
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return users

# 사용자 정보 업데이트 (PUT)
@app.put("/users/update")
def update_user(user: UserUpdate):
    conn = None
    cursor = None
    try:
        db_dk = DB_docking()
        conn = db_dk.connection
        cursor = conn.cursor()
        db_dk.update_user_cursor(cursor, user.name, user.email, user.id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return {"id": user.id, "name": user.name, "email": user.email}

# 사용자 id 정보 업데이트 (PUT)
@app.put("/users/update/id")
def update_user(user: UserUpdate):
    conn = None
    cursor = None
    try:
        db_dk = DB_docking()
        conn = db_dk.connection
        cursor = conn.cursor()
        db_dk.update_user_id_cursor(cursor, user.email, user.id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return {"id": user.id, "name": user.name, "email": user.email}

# 사용자 삭제 (DELETE)
@app.delete("/users/delete/")
def delete_user(user: UserDelete):
    conn = None
    cursor = None
    try:
        db_dk= DB_docking()
        conn = db_dk.connection
        cursor = conn.cursor()
        db_dk.delete_user_cursor(cursor, user.id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)