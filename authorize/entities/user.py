from rest_framework.exceptions import NotFound

from authorize.entities.repository import IRepository

from ..models import User


class UserRepository(IRepository):

    @staticmethod
    def get_by_id(user_id):
        try:
            member = User.objects.get(pk=user_id)
            return member

        except User.DoesNotExist:
            raise NotFound(detail="User not found")

