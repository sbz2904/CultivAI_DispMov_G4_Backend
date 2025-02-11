from config.mongo_config import db
from bson import ObjectId
from gridfs import GridFS
from flask import request, jsonify
import datetime

fs = GridFS(db)

def add_sembrio(data):
    try:
        sembrio_ref = db.sembrios.insert_one(data) 
        return {'id': str(sembrio_ref.inserted_id)}
    except Exception as e:
        return {'error': str(e)}

def get_all_sembrios():
    try:
        sembríos = []
        for doc in db.sembrios.find():
            doc['_id'] = str(doc['_id'])
            sembríos.append(doc)
        return sembríos
    except Exception as e:
        return {'error': str(e)}

def get_sembrio_by_id(sembrio_id):
    try:
        doc = db.sembrios.find_one({'_id': ObjectId(sembrio_id)})
        if doc:
            doc['_id'] = str(doc['_id']) 
            return doc
        return {'error': 'Sembrío no encontrado'}
    except Exception as e:
        return {'error': str(e)}

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
            sembrio_ids = user.get('sembrios', []) 
            sembrios = list(db.sembrios.find({'_id': {'$in': [ObjectId(id) for id in sembrio_ids]}}))
            for sembrio in sembrios:
                sembrio['_id'] = str(sembrio['_id'])  
            return {'sembrios': sembrios}
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}
    
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

def upload_image(sembrio_id, user_id):
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({'error': 'El archivo es obligatorio'}), 400
        
        file_id = fs.put(file, filename=file.filename, metadata={'user_id': str(user_id), 'sembrio_id': str(sembrio_id)})
        return jsonify({'message': 'Imagen subida', 'file_id': str(file_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

def delete_note(sembrio_id, user_id, note_id):
    try:
        result = db.notas.delete_one({
            '_id': ObjectId(note_id),
            'user_id': ObjectId(user_id),
            'sembrio_id': ObjectId(sembrio_id)
        })
        if result.deleted_count > 0:
            return jsonify({'message': 'Nota eliminada correctamente'}), 200
        return jsonify({'error': 'Nota no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_image(file_id, user_id, sembrio_id):
    try:
        image = db.fs.files.find_one({'_id': ObjectId(file_id), 'metadata.user_id': str(user_id), 'metadata.sembrio_id': str(sembrio_id)})
        if not image:
            return jsonify({'error': 'Imagen no encontrada'}), 404

        fs.delete(ObjectId(file_id))
        return jsonify({'message': 'Imagen eliminada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


