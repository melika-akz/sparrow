from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authorize.views import TokenController


urlpatterns = [
    path('', TokenController.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(),  name='token_refresh'),
]

