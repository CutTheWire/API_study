from locust import HttpUser, task, between
import uuid

class UserBehavior(HttpUser):
    host = "http://192.168.45.154:8000/"
    wait_time = between(1, 2)

    @task
    def create_and_delete_user(self):
        # 유니크한 사용자 ID 생성
        user_id = str(uuid.uuid4())
        # 사용자 정보
        user_data = {
            "id": user_id,
            "name": "Test User",
            "email": f"{user_id}@example.com",
            "created_at": "2024-05-12T00:00:00"  # ISO 8601 형식
        }
        # 사용자 생성
        with self.client.post("users/create", json=user_data, catch_response=True) as response:
            if response.status_code == 200:
                # 생성된 사용자 삭제
                self.client.delete(f"users/delete/", json={"id": user_id})
            else:
                response.failure(f"Failed to create user: {response.status_code}")
