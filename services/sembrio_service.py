from config.firebase_config import db

def add_sembrio(data):
    try:
        sembrio_ref = db.collection('sembríos').add(data)
        return {'id': sembrio_ref[1].id}
    except Exception as e:
        return {'error': str(e)}

def get_all_sembríos():
    try:
        sembríos = [doc.to_dict() | {'id': doc.id} for doc in db.collection('sembríos').stream()]
        return sembríos
    except Exception as e:
        return {'error': str(e)}
