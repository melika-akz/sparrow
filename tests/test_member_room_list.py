import pytest

from messenger.constants import DIRECT, GROUP, CHANNEL
from messenger.models import RoomMember, Room
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

        cls.group1 = Room.objects.create(
            name='group 1',
            type=GROUP,
        )

        RoomMember.objects.create(
            room=cls.group1,
            member=cls.member
        )
        RoomMember.objects.create(
            room=cls.group1,
            member=cls.member2
        )

        cls.group2 = Room.objects.create(
            name='group 2',
            type=GROUP,
        )

        RoomMember.objects.create(
            room=cls.group2,
            member=cls.member3
        )

        cls.channel = Room.objects.create(
            name='group 3',
            type=CHANNEL,
        )

        RoomMember.objects.create(
            room=cls.channel,
            member=cls.member
        )

        cls.direct3 = Room.objects.create(
            name='direct 3',
            type=DIRECT,
        )

        RoomMember.objects.create(
            room=cls.direct3,
            member=cls.member2
        )
        RoomMember.objects.create(
            room=cls.direct3,
            member=cls.member3
        )

    def test_list(self):
        self.login(self.member)
        response = self._client(
            'Get a list of direct current member',
            path='/apiv1/messenger/member/rooms/',
            method='GET',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 2
        for data in response.data['results']:
            assert data['id'] in [self.group1.id, self.channel.id]
            assert data['type'] in [GROUP, CHANNEL]

