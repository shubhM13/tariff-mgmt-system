from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(uid, pswd):
    user = UserModel.find_by_id(uid)
    if user and safe_str_cmp(user.pswd, pswd):
        return user
    else:
        return None

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
