from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings


def generate_jwt_token(member):
    payload = {
        'id': member.id,
        'title': member.title,
        'first_name': member.first_name,
        'last_name': member.last_name,
        'email': member.email,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'iat': datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token

