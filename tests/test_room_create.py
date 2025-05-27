import pytest

from apis.constants import GROUP
from apis.models import RoomMember
from authorize.models import Member
from .helpers import BaseTestCase


class TestRoom(BaseTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.member = Member.objects.create_user(
            title='member',
            first_name='member first name',
            last_name='member last name',
            email='member@example.com',
            password='123456',
        )
        cls.member2 = Member.objects.create_user(
            title='member2',
            first_name='member 2 first name',
            last_name='member 2 last name',
            email='member2@example.com',
            password='123456',
        )

    def test_create(self):
        self.login(self.member)

        response = self._client(
            'Trying to create a group',
            path='/sparrow/apiv1/rooms/',
            method='POST',
            data=dict(
                type=GROUP,
                members=[self.member2.id],
                name='The Group Name'
            ),
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['name'] == 'The Group Name'
        assert response.data['type'] == GROUP

        room_member = RoomMember.objects.filter(room_id=response.data['id'])
        for member in room_member:
            assert member.id in [self.member2.id, self.member.id]

