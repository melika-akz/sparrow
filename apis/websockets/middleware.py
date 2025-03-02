from urllib.parse import parse_qs
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

class TokenAuthMiddleware:
    """Middleware to authenticate users via WebSocket token."""

    def __init__(self, inner):
        self.inner = inner  # The next middleware or consumer

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token_key = query_string.get("token", [None])[0]  # Extract token

        if token_key:
            try:
                scope["user"] = Token.objects.get(key=token_key).user
            except:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
