from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # ✅ Import this

# Initialize Flask App
app = Flask(__name__)

# Load Configurations
app.config.from_object("app.config.Config")

# Initialize Database
db = SQLAlchemy(app)

# Test Connection
with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))  # ✅ Wrap SQL query with text()
        print("✅ SQLAlchemy is connected to PostgreSQL!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

# Define a Simple Route
@app.route("/")
def home():
    return "🚀 AI Resume Screener is Running!"

if __name__ == '__main__':
    app.run(debug=True, port=5006)