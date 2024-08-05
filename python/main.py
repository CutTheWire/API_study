from datetime import timedelta, datetime
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from utils.auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, hash_password
from utils.database import create_user, get_user_by_id, get_day_all, update_user_token
from utils.schemas import UserCreate, UserResponse, LoginResponse, ThroughputDayAllResponse

app = FastAPI()

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate):
    db_user = get_user_by_id(user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    user_id = create_user(user)
    
    # 사용자 정보 가져오기
    db_user = get_user_by_id(user.user_id)  # 사용자 정보 다시 조회
    
    if db_user is None:
        raise HTTPException(status_code=500, detail="User creation failed")
    
    return UserResponse(
        user_idx=db_user['user_idx'],
        user_id=db_user['user_id'],
        user_name=db_user['user_name'],
        phone_number=db_user.get('phone_number', None)
    )


@app.post("/login", response_model=LoginResponse)
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
    
    # 토큰과 만료 시간 업데이트
    update_user_token(user_id=user_id, token=access_token, expires_at=datetime.now() + access_token_expires)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )


@app.get("/throughput/day/all", response_model=ThroughputDayAllResponse)
def throughputDayAll(iotId: str, date: str):
    db_data = get_day_all(iotId, date)
    if not db_data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return ThroughputDayAllResponse(
        id=db_data['id'],
        iotId=db_data['iot_id'],
        measuredWeight=db_data['measured_weight'],
        timeStamp=db_data['timestamp'],
        status=db_data['status'],
    )

# 일별 데이터 불러오기
# @app.get("/throughout/day/all")
# async def get_day_all(data: GetDeviceToken):
#     try:
#         result = db_queries.get_day_all_cursor(data.iotId)
#         if not result:
#             raise HTTPException(status_code=404, detail="No data found for the provided IoT ID")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return result



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
