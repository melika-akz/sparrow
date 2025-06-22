import pytest
from django.core.cache import cache
from rest_framework import status

from messenger.constants import DIRECT
from messenger.models import RoomMember, Room, Message
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

        cls.direct2 = Room.objects.create(
            name='direct 2',
            type=DIRECT,
        )

        RoomMember.objects.create(
            room=cls.direct2,
            member=cls.member2
        )
        RoomMember.objects.create(
            room=cls.direct2,
            member=cls.member3
        )

        cls.message1 = Message.objects.create(
            body='Hello!',
            sender=cls.member,
            room=cls.direct1,
        )
        cls.message2 = Message.objects.create(
            body='this is a message2',
            sender=cls.member,
            room=cls.direct1,
        )

    def test_get_count(self):
        self.login(self.member)

        response = self._client(
            'Trying to get a count of message from room',
            path=f'/apiv1/messenger/rooms/{self.direct1.id}/messages/counts/',
            method='Get',
        )
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data['count'] == 2

        response = self._client(
            'Trying to get a not found room messages',
            path=f'/apiv1/messenger/rooms/0/messages/',
            method='GET',
        )
        assert response.status_code == 404

        self.logout()
        response = self._client(
            'Unauthorize request',
            path=f'/apiv1/members/{self.member.id}/',
            method='GET',
        )
        assert response.status_code == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

