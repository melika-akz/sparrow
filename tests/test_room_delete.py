import pytest

from apis.constants import DIRECT, GROUP
from apis.models import RoomMember, Room
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
        cls.member3 = Member.objects.create_user(
            title='member3',
            first_name='member 3 first name',
            last_name='member 3 last name',
            email='member3@example.com',
            password='123456',
        )

        cls.direct1 = Room.objects.create(
            name='direct 1',
            type=DIRECT,
        )

        RoomMember.objects.create(
            room=cls.direct1,
            member=cls.member
        )
        RoomMember.objects.create(
            room=cls.direct1,
            member=cls.member2
        )

        cls.group = Room.objects.create(
            name='group 1',
            type=GROUP,
        )

        RoomMember.objects.create(
            room=cls.group,
            member=cls.member
        )
        RoomMember.objects.create(
            room=cls.group,
            member=cls.member3
        )

        cls.group2 = Room.objects.create(
            name='group 2',
            type=GROUP,
        )

        RoomMember.objects.create(
            room=cls.group2,
            member=cls.member2
        )
        RoomMember.objects.create(
            room=cls.group2,
            member=cls.member3
        )
        RoomMember.objects.create(
            room=cls.group2,
            member=cls.member
        )

        cls.group3 = Room.objects.create(
            name='group 3',
            type=GROUP,
        )

        RoomMember.objects.create(
            room=cls.group3,
            member=cls.member2
        )
        RoomMember.objects.create(
            room=cls.group3,
            member=cls.member3
        )

    def test_delete(self):
        self.login(self.member)

        response = self._client(
            'Trying to delete a group',
            path=f'/sparrow/apiv1/rooms/{self.group.id}/',
            method='DELETE',
        )
        assert response.status_code == 204

