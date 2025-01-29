from config.firebase_config import db

def create_user(data):
    try:
        user_ref = db.collection('usuarios').add(data)
        return {'id': user_ref[1].id}
    except Exception as e:
        return {'error': str(e)}

def get_all_users():
    try:
        users = [doc.to_dict() | {'id': doc.id} for doc in db.collection('usuarios').stream()]
        return users
    except Exception as e:
        return {'error': str(e)}

def get_user_by_id(user_id):
    try:
        doc = db.collection('usuarios').document(user_id).get()
        if doc.exists:
            return doc.to_dict() | {'id': doc.id}
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}
