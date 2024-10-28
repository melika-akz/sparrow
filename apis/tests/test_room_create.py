import json

import pytest
from rest_framework.test import APITransactionTestCase

from authorize.helpers import generate_jwt_token
from authorize.models import User
from .helpers import _client
from ..models import RoomMember


class TestRoom(APITransactionTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.user = User.objects.create_user(
            title='member',
            first_name='member first name',
            last_name='member last name',
            email='member@example.com',
            password='123456',
        )
        cls.user2 = User.objects.create_user(
            title='member2',
            first_name='member 2 first name',
            last_name='member 2 last name',
            email='member2@example.com',
            password='123456',
        )

    def test_create(self):
        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        response = _client(
            self,
            path='/apiv1/rooms/',
            method='POST',
            data=dict(
                type='D',
                member_id=2,
            ),
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['name'] == 'member 2 first name member 2 last name'
        assert response.data['type'] == 'D'

        room_member = RoomMember.objects.filter(room_id=response.data['id'])
        for member in room_member:
            assert member.id in [self.user2.id, self.user.id]

        response = _client(
            self,
            path='/apiv1/rooms/',
            method='POST',
            data=dict(
                type='D',
                member_id=1,
            ),
        )
        assert response.status_code == 400
        self.assertEqual(response.data['detail'], 'You cannot create a room to chat with yourself.')



