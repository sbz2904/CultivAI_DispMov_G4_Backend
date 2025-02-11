from bson import ObjectId
from config.mongo_config import db
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(data):
    try:
        if 'password' in data:
            data['password'] = hash_password(data['password'])

        user_ref = db.usuarios.insert_one(data)
        return {'id': str(user_ref.inserted_id)}
    except Exception as e:
        return {'error': str(e)}
        
def get_all_users():
    try:
        users = []
        for doc in db.usuarios.find():
            doc['_id'] = str(doc['_id'])
            users.append(doc)
        return users 
    except Exception as e:
        return {'error': str(e)}
    
def get_user_by_email(email):
    try:
        user = db.usuarios.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id']) 
            user['sembrios'] = user.get('sembrios', []) 
            return user
        return None
    except Exception as e:
        return {'error': str(e)}

def get_user_by_id(user_id):
    try:
        user = db.usuarios.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])  
            user['sembrios'] = user.get('sembrios', []) 
            return user
        return {'error': 'Usuario no encontrado'}
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

def update_user(user_id, data):
    try:
        result = db.usuarios.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        if result.matched_count > 0:
            return {'message': 'Usuario actualizado correctamente'}
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}
