import pytest
from rest_framework.test import APITransactionTestCase

from apis.constants import DIRECT
from apis.models import RoomMember, Room
from authorize.helpers import generate_jwt_token
from authorize.models import Member

from .helpers import _client


class TestRoom(APITransactionTestCase):

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

    def test_send(self):
        self.jwt_token = generate_jwt_token(self.member.id)
        self.client.force_authenticate(user=self.member, token=self.jwt_token)

        response = _client(
            self,
            path=f'/sparrow/apiv1/rooms/{self.direct1.id}/messages',
            method='POST',
            data=dict(body='this is a message'),
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['body'] == 'this is a message'
        assert response.data['sender_id'] == self.member.id
        assert response.data['created_at'] is not None
        assert response.data['seen_at'] is None
        assert response.data['room_id'] == self.direct1.id

        response = _client(
            self,
            path=f'/sparrow/apiv1/rooms/{self.direct2.id}/messages',
            method='POST',
            data=dict(body='this is a message'),
        )
        assert response.status_code == 400
