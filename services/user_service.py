#from config.firebase_config import db
from bson import ObjectId

from config.mongo_config import db

def create_user(data):
    try:
        #user_ref = db.collection('usuarios').add(data)
        user_ref = db.usuarios.insert_one(data)
        #return {'id': user_ref[1].id}
        return {'id': user_ref[1].get('_id')}
    except Exception as e:
        return {'error': str(e)}

def get_all_users():
    try:
        # users = [doc.to_dict() | {'id': doc.id} for doc in db.collection('usuarios').stream()]
        users = [doc.to_dict() | {'id': doc.get('_id')} for doc in db.usuarios.find()]
        return users
    except Exception as e:
        return {'error': str(e)}

def get_user_by_id(user_id):
    try:
        #doc = db.collection('usuarios').document(user_id).get()
        doc = db.usuarios.find_one({'_id': ObjectId(user_id)})
        if doc.exists:
            return doc.to_dict() | {'id': doc.get('_id')}
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}
