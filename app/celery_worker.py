from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0"
)

@celery.task
def send_alert(transaction_id):
    print(f"ALERT: High risk transaction {transaction_id}")
