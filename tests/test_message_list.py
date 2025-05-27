import pytest
from django.core.cache import cache

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

    def test_list(self):
        self.login(self.member)

        cache_key = f"messages_room_{self.direct1.id}"
        cache.delete(cache_key)

        response = self._client(
            'Trying to get a list of message from room',
            path=f'/apiv1/messenger/rooms/{self.direct1.id}/messages/',
            method='Get',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 2
        for data in response.data['results']:
            assert data['id'] is not None
            assert data['body'] is not None
            assert data['sender_id'] == self.member.id
            assert data['created_at'] is not None
            assert data['seen_at'] is None
            assert data['room_id'] == self.direct1.id

        assert cache.get(cache_key) is not None

        response = self._client(
            'Trying to search a message by body',
            path=f'/apiv1/messenger/rooms/{self.direct1.id}/messages/?search=Hello',
            method='Get',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        data = response.data['results'][0]
        assert data['id'] is not None
        assert data['body'] is not None
        assert data['sender_id'] == self.member.id
        assert data['created_at'] is not None
        assert data['seen_at'] is None
        assert data['room_id'] == self.direct1.id

        response = self._client(
            'Trying to get a not found room messages',
            path=f'/apiv1/messenger/rooms/0/messages/',
            method='GET',
        )
        assert response.status_code == 404

