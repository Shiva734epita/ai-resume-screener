from app import create_app
from app.celery_worker import celery

app = create_app()

# Bind Celery to Flask app context
app.app_context().push()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5006)
