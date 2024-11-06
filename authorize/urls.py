from django.urls import path

from authorize.views import MemberView, TokenController, MemberDetailView

urlpatterns = [
    path('tokens/', TokenController.as_view(), name='token_obtain_pair'),
    path('members/', MemberView.as_view(), name='register_member'),
    path('members/<int:member_id>/', MemberView.as_view(), name='update_member'),
    path('members/<int:member_id>/', MemberDetailView.as_view(), name='update_member'),
]

