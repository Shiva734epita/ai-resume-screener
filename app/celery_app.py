from celery import Celery
from flask import Flask

def create_celery():
    """Initialize Celery without circular dependencies"""
    flask_app = Flask(__name__)
    flask_app.config.from_object("app.config")  # ✅ Load configuration from a separate file

    # ✅ Initialize Celery with Flask settings
    celery = Celery(
        flask_app.import_name,
        broker=flask_app.config.get("CELERY_BROKER_URL", "redis://localhost:6380/0"), 
        backend=flask_app.config.get("RESULT_BACKEND", "redis://localhost:6380/0")
    )

    celery.conf.update(flask_app.config)
    celery.conf.update(
        task_default_queue="celery",
        worker_redirect_stdouts_level="DEBUG",
        worker_log_color=False,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json"
    )

    class ContextTask(celery.Task):
        """Attach Flask app context to Celery tasks"""
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask  

    import app.tasks

    return celery

# ✅ Create Celery Instance without Flask circular import issues
celery = create_celery()
