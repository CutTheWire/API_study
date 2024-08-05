from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from utils.auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, hash_password
from utils.database import create_user, get_user_by_id
from utils.schemas import UserCreate, UserResponse

app = FastAPI()

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate):
    db_user = get_user_by_id(user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    user_id = create_user(user)
    return {
        "user_id": user_id,
        "user_name": user.user_name,
        "phone_number": user.phone_number
    }

@app.post("/login")
def login(user_id: str, pw: str):
    db_user = get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(pw, db_user['pw']):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user['user_id']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
