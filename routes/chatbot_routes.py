from flask import Blueprint, request, jsonify
from services.chatbot_service import ask_chatbot

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/', methods=['POST'])
def ask_chatbot_route():
    data = request.get_json()
    message = data.get('message')
    weather_data = data.get('weather_data', {})
    result = ask_chatbot(message, weather_data)
    return jsonify(result), 200 if 'error' not in result else 500
