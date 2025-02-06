from config.mongo_config import db
from bson import ObjectId
from gridfs import GridFS
from flask import request, jsonify
import datetime

fs = GridFS(db)

# ✅ Agregar un nuevo sembrío
def add_sembrio(data):
    try:
        sembrio_ref = db.sembrios.insert_one(data)  # Insertar en MongoDB
        return {'id': str(sembrio_ref.inserted_id)}  # Convertir ObjectId a string
    except Exception as e:
        return {'error': str(e)}

# ✅ Obtener todos los sembríos
def get_all_sembrios():
    try:
        sembríos = []
        for doc in db.sembrios.find():
            doc['_id'] = str(doc['_id'])  # Convertir ObjectId a string
            sembríos.append(doc)
        return sembríos
    except Exception as e:
        return {'error': str(e)}

# ✅ Obtener un sembrío por ID
def get_sembrio_by_id(sembrio_id):
    try:
        doc = db.sembrios.find_one({'_id': ObjectId(sembrio_id)})
        if doc:
            doc['_id'] = str(doc['_id'])  # Convertir ObjectId a string
            return doc
        return {'error': 'Sembrío no encontrado'}
    except Exception as e:
        return {'error': str(e)}

# ✅ Guardar sembríos de un usuario (asociar sembríos a un usuario)
def update_user_sembrios(user_id, sembrios_ids):
    try:
        result = db.usuarios.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'sembrios': sembrios_ids}}
        )
        if result.matched_count > 0:
            return {'message': 'Sembrios actualizados correctamente'}
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}

def get_user_sembrios(user_id):
    try:
        user = db.usuarios.find_one({'_id': ObjectId(user_id)})
        if user:
            sembrio_ids = user.get('sembrios', [])  # Obtener IDs de los sembríos
            sembrios = list(db.sembrios.find({'_id': {'$in': [ObjectId(id) for id in sembrio_ids]}}))
            for sembrio in sembrios:
                sembrio['_id'] = str(sembrio['_id'])  # Convertir ObjectId a string
            return {'sembrios': sembrios}
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}
    
# ✅ Guardar una nueva nota asociada a un usuario y sembrío
def add_note(sembrio_id, user_id):
    try:
        data = request.get_json()
        content = data.get('content')
        timestamp = datetime.datetime.utcnow()
        
        if not content:
            return jsonify({'error': 'El contenido de la nota es obligatorio'}), 400
        
        note = {
            'user_id': ObjectId(user_id),
            'sembrio_id': ObjectId(sembrio_id),
            'content': content,
            'timestamp': timestamp
        }
        db.notas.insert_one(note)
        return jsonify({'message': 'Nota guardada con éxito'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Obtener todas las notas de un usuario para un sembrío
def get_notes(sembrio_id, user_id):
    try:
        notas = list(db.notas.find({'user_id': ObjectId(user_id), 'sembrio_id': ObjectId(sembrio_id)}))
        for nota in notas:
            nota['_id'] = str(nota['_id'])
            nota['user_id'] = str(nota['user_id'])
            nota['sembrio_id'] = str(nota['sembrio_id'])
        return jsonify(notas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Subir imagen a GridFS asociada a un usuario y sembrío
def upload_image(sembrio_id, user_id):
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({'error': 'El archivo es obligatorio'}), 400
        
        file_id = fs.put(file, filename=file.filename, metadata={'user_id': str(user_id), 'sembrio_id': str(sembrio_id)})
        return jsonify({'message': 'Imagen subida', 'file_id': str(file_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Obtener imágenes de un usuario para un sembrío
def get_images(sembrio_id, user_id):
    try:
        images = db.fs.files.find({'metadata.user_id': str(user_id), 'metadata.sembrio_id': str(sembrio_id)})
        image_list = [
            {
                "file_id": str(img['_id']),
                "filename": img['filename'],
                "url": f"http://192.168.100.2:5000/api/sembrios/imagenes/{str(img['_id'])}"
            }
            for img in images
        ]
        return jsonify(image_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Eliminar una imagen de GridFS
def delete_image(sembrio_id, file_id):
    try:
        fs.delete(ObjectId(file_id))
        return jsonify({'message': 'Imagen eliminada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Eliminar una nota

def delete_note(sembrio_id, nota_id):
    try:
        result = db.notas.delete_one({'_id': ObjectId(nota_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Nota eliminada'}), 200
        return jsonify({'error': 'Nota no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

