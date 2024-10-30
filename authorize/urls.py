from django.urls import path

from authorize.views import TokenController, RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', TokenController.as_view(), name='token_obtain_pair'),
]

