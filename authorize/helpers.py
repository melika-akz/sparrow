import jwt

from sparrow.settings import SECRET_KEY


def generate_jwt_token(member_id):
    payload = {
        'member_id': member_id,
    }
    secret_key = SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

