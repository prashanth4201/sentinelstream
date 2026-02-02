from locust import HttpUser, task, between

class SentinelStreamUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def create_transaction(self):
        self.client.post(
            "/transaction",
            json={
                "user_id": 1,
                "amount": 15000
            }
        )
