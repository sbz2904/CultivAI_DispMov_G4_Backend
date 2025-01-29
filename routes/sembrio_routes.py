from flask import Blueprint, request, jsonify
from services.sembrio_service import add_sembrio, get_all_sembríos

sembrio_bp = Blueprint('sembrio_bp', __name__)

@sembrio_bp.route('/', methods=['POST'])
def add_sembrio_route():
    data = request.get_json()
    result = add_sembrio(data)
    return jsonify(result), 201 if 'id' in result else 500

@sembrio_bp.route('/', methods=['GET'])
def get_all_sembríos_route():
    result = get_all_sembríos()
    return jsonify(result), 200 if isinstance(result, list) else 500
