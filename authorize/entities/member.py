from rest_framework.exceptions import NotFound

from authorize.entities.repository import IRepository

from ..models import Member


class MemberRepository(IRepository):

    @staticmethod
    def get_by_id(member_id):
        try:
            member = Member.objects.get(pk=member_id)
            return member

        except Member.DoesNotExist:
            raise NotFound(detail="Member not found")

