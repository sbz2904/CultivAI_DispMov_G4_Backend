from flask import Blueprint, request, jsonify
from services.weather_service import get_weather

weather_bp = Blueprint('weather_bp', __name__)

@weather_bp.route('/', methods=['GET'])
def get_weather_route():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    result = get_weather(latitude, longitude)
    return jsonify(result), 200 if 'error' not in result else 500
