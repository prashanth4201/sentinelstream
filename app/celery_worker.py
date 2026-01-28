from celery import Celery

celery = Celery(
    "sentinel",
    	broker="redis://localhost:6379/0",
	backend="redis://localhost:6379/0"

)

@celery.task
def fraud_alert(data):
    print("🚨 FRAUD ALERT:", data)
