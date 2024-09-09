from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import DRFTokenSerializer


class TokenController(TokenObtainPairView):
    serializer_class = DRFTokenSerializer

