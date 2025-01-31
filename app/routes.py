from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/health-check', methods=['GET'])
def health_check():
    return {"status": "Flask is running!"}, 200
