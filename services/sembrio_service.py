#from config.firebase_config import db
from config.mongo_config import db

def add_sembrio(data):
    try:
        #sembrio_ref = db.collection('sembríos').add(data)
        sembrio_ref = db.sembrio.insert_one(data)
        return {'id': sembrio_ref[1].id}
    except Exception as e:
        return {'error': str(e)}

def get_all_sembríos():
    try:
        #sembríos = [doc.to_dict() | {'id': doc.id} for doc in db.collection('sembríos').stream()]
        sembríos = [doc.to_dict() | {'id': doc.get('_id')} for doc in list(db.sembrios.find())]
        return sembríos
    except Exception as e:
        return {'error': str(e)}
