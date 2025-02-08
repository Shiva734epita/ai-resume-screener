from app.celery_app import celery  # ✅ Import only Celery, not Flask app

if __name__ == "__main__":
    celery.start()
