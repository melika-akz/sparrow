import pytest
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from authorize.helpers import generate_jwt_token
from authorize.models import Member

from .helpers import _client


class TestMember(APITransactionTestCase):

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

    def test_get(self):
        """Get a Member"""
        response = _client(
            self,
            path='/apiv1/members/1/',
            method='GET',
        )
        assert response.status_code == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.jwt_token = generate_jwt_token(self.member.id)
        self.client.force_authenticate(user=self.member, token=self.jwt_token)

        response = _client(
            self,
            path=f'/apiv1/members/1/',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['id'] == self.member.id

        response = _client(
            self,
            path=f'/apiv1/members/0/',
            method='GET',
        )
        assert response.status_code == 404

