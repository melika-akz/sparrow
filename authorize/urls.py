from django.urls import path

from authorize.views import MemberView, TokenController, MemberDetailView, SelfView, GoogleAuthView, GoogleCallbackView


urlpatterns = [
    path('tokens/', TokenController.as_view(), name='token_obtain_pair'),
    path('members/', MemberView.as_view(), name='members'),
    path('members/<int:member_id>/', MemberDetailView.as_view(), name='detail_member'),
    path('self/', SelfView.as_view(), name='self'),
    path('auth/google/', GoogleAuthView.as_view(), name='auth-google'),
    path('auth/google/callback/', GoogleCallbackView.as_view(), name='callback-google'),
]

