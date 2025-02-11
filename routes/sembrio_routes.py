from flask import Blueprint, request, jsonify, send_file
from services.sembrio_service import add_sembrio, get_all_sembrios, get_sembrio_by_id, get_user_sembrios, update_user_sembrios, add_note, get_notes, upload_image, get_images, fs, delete_note, delete_image
from services.user_service import get_user_by_id
from io import BytesIO
from bson import ObjectId

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

# ✅ Guardar una nueva nota
@sembrio_bp.route('/<string:sembrio_id>/notas/<string:user_id>', methods=['POST'])
def add_note_route(sembrio_id, user_id):
    return add_note(sembrio_id, user_id)

# ✅ Obtener todas las notas de un usuario para un sembrío
@sembrio_bp.route('/<string:sembrio_id>/notas/<string:user_id>', methods=['GET'])
def get_notes_route(sembrio_id, user_id):
    return get_notes(sembrio_id, user_id)

# ✅ Subir imagen a GridFS
@sembrio_bp.route('/<string:sembrio_id>/imagenes/<string:user_id>', methods=['POST'])
def upload_image_route(sembrio_id, user_id):
    return upload_image(sembrio_id, user_id)

# ✅ Obtener imágenes de un usuario para un sembrío
@sembrio_bp.route('/<string:sembrio_id>/imagenes/<string:user_id>', methods=['GET'])
def get_images_route(sembrio_id, user_id):
    return get_images(sembrio_id, user_id)


@sembrio_bp.route('/imagenes/<string:file_id>', methods=['GET'])
def get_image(file_id):
    try:
        file = fs.get(ObjectId(file_id))
        return send_file(BytesIO(file.read()), mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    
# ✅ Eliminar una nota
@sembrio_bp.route('/<string:sembrio_id>/notas/<string:user_id>/<string:note_id>', methods=['DELETE'])
def delete_note_route(sembrio_id, user_id, note_id):
    return delete_note(sembrio_id, user_id, note_id)

# ✅ Eliminar una imagen
@sembrio_bp.route('/imagenes/<string:file_id>/<string:user_id>/<string:sembrio_id>', methods=['DELETE'])
def delete_image_route(file_id, user_id, sembrio_id):
    return delete_image(file_id, user_id, sembrio_id)
