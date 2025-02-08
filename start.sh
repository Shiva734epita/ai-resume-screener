#!/bin/bash

echo "🛑 Stopping all existing services..."

# Kill Redis (if running)
REDIS_PID=$(pgrep redis-server)
if [ -n "$REDIS_PID" ]; then
    echo "❌ Stopping Redis..."
    kill -9 $REDIS_PID
fi

# Kill Celery Worker (if running)
CELERY_PID=$(pgrep -f "celery worker")
if [ -n "$CELERY_PID" ]; then
    echo "❌ Stopping Celery Worker..."
    kill -9 $CELERY_PID
fi

# Kill Flask (if running)
FLASK_PID=$(pgrep -f "flask run")
if [ -n "$FLASK_PID" ]; then
    echo "❌ Stopping Flask Backend..."
    kill -9 $FLASK_PID
fi

# Kill Python App (if running)
PYTHON_PID=$(pgrep -f "python app.py")
if [ -n "$PYTHON_PID" ]; then
    echo "❌ Stopping Python Application..."
    kill -9 $PYTHON_PID
fi

echo "✅ All services stopped!"

# Wait for cleanup
sleep 2

echo "🚀 Starting Redis on port 6380..."
redis-server --port 6380 &

sleep 2  # Wait for Redis to start

echo "🔄 Starting Celery Worker..."
celery -A app.celery_app.celery worker --loglevel=info &

sleep 2  # Wait for Celery to initialize

echo "🔥 Starting Flask Backend..."
flask run --port 5006 &

sleep 2  # Wait for Flask to stabilize

echo "🐍 Running Python Application..."
python app.py &  # ✅ Runs your Python application

echo "✅ All services restarted! Press Ctrl+C to stop."
wait  # Keeps the script running
