import pytest
from rest_framework.test import APITransactionTestCase

from apis.constants import DIRECT
from apis.models import RoomMember
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

    def test_create(self):
        self.jwt_token = generate_jwt_token(self.member.id)
        self.client.force_authenticate(user=self.member, token=self.jwt_token)

        response = _client(
            self,
            path='/sparrow/apiv1/directs/',
            method='POST',
            data=dict(
                type=DIRECT,
                member_id=self.member2.id,
            ),
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['name'] == 'member 2 first name member 2 last name'
        assert response.data['type'] == DIRECT

        room_member = RoomMember.objects.filter(room_id=response.data['id'])
        for member in room_member:
            assert member.id in [self.member2.id, self.member.id]

        response = _client(
            self,
            path='/sparrow/apiv1/directs/',
            method='POST',
            data=dict(
                type=DIRECT,
                member_id=1,
            ),
        )
        assert response.status_code == 400
        self.assertEqual(response.data['detail'], 'You cannot create a direct with yourself.')

