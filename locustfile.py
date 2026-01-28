from locust import HttpUser, task, between

class TransactionUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def send_transaction(self):
        self.client.post(
            "/transaction",
            json={
                "user_id": 1,
                "amount": 3000
            }
        )
