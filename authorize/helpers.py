import jwt

from sparrow.settings import SECRET_KEY


def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
    }
    secret_key = SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

