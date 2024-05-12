from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    # 기본 호스트 URL 지정
    # host = "http://localhost:8000/"
    host = "http://192.168.219.101:8008/"
    # 사용자가 다음 작업을 수행하기 전에 대기하는 시간(초 단위)
    wait_time = between(1, 2)

    @task
    def get_users(self):
        # "/users/" 경로에 대한 GET 요청 수행
        # self.client.get("users/")
        self.client.get("PrintAllUser/")