from flask import Blueprint, request, jsonify
from services.user_service import create_user, get_all_users, get_user_by_id, update_user, get_user_by_email, verify_password

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['POST'])
def create_user_route():
    data = request.get_json()
    result = create_user(data)
    return jsonify(result), 201 if 'id' in result else 500

@user_bp.route('/', methods=['GET'])
def get_all_users_route():
    result = get_all_users()
    return jsonify(result), 200 if isinstance(result, list) else 500

@user_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id_route(user_id):
    result = get_user_by_id(user_id)
    return jsonify(result), 200 if '_id' in result else 404

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.get_json()
    result = update_user(user_id, data)
    return jsonify(result), 200 if 'message' in result else 404

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = get_user_by_email(email)
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Verificamos la contraseña
    if not verify_password(password, user['password']):
        return jsonify({'error': 'Contraseña incorrecta'}), 401

    return jsonify({'message': 'Inicio de sesión exitoso', 'user_id': user['_id']}), 200