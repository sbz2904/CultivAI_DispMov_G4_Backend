from flask import Blueprint, request, jsonify
from services.sembrio_service import add_sembrio, get_all_sembrios, get_sembrio_by_id, get_user_sembrios, update_user_sembrios
from services.user_service import get_user_by_id

sembrio_bp = Blueprint('sembrio_bp', __name__)

# ✅ Obtener todos los sembríos
@sembrio_bp.route('/', methods=['GET'])
def get_all_sembrios_route():
    result = get_all_sembrios()
    return jsonify(result), 200 if isinstance(result, list) else 500

# ✅ Obtener un sembrío por ID
@sembrio_bp.route('/<string:sembrio_id>', methods=['GET'])
def get_by_id(sembrio_id):
    result = get_sembrio_by_id(sembrio_id)
    return jsonify(result), 200 if '_id' in result else 404

# ✅ Agregar un nuevo sembrío
@sembrio_bp.route('/', methods=['POST'])
def add_sembrio_route():
    data = request.get_json()
    result = add_sembrio(data)
    return jsonify(result), 201 if 'id' in result else 500

# ✅ Obtener los sembríos de un usuario con detalles
@sembrio_bp.route('/users/<string:user_id>/sembrios', methods=['GET'])
def get_user_sembrios_route(user_id):
    result = get_user_sembrios(user_id)  # Usa la versión corregida de `get_user_sembrios`
    return jsonify(result), 200 if 'sembrios' in result else 500

# ✅ Actualizar sembríos de un usuario
@sembrio_bp.route('/users/<string:user_id>/sembrios', methods=['PUT'])
def update_user_sembrios_route(user_id):
    data = request.get_json()
    result = update_user_sembrios(user_id, data.get('sembrios', []))  # Consistencia en clave
    return jsonify(result), 200 if 'message' in result else 500
