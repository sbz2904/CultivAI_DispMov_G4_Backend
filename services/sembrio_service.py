from config.mongo_config import db
from bson import ObjectId

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