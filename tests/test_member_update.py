import pytest
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from authorize.helpers import generate_jwt_token
from authorize.models import User

from .helpers import _client


class TestMember(APITransactionTestCase):

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

    def test_update(self):
        """Updating Member"""
        response = _client(
            self,
            path='/apiv1/members/1/',
            method='PUT',
            data=dict(
                title='member2',
                first_name='member first name',
                last_name='member last name',
                email='member@example.com',
                password='123456',
            ),
        )
        assert response.status_code == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        response = _client(
            self,
            path=f'/apiv1/members/{self.user.id}/',
            method='PUT',
            data=dict(
                title='new title',
                first_name='member first name',
                last_name='member last name',
                email='member@example.com',
                password='123456',
            ),
        )
        assert response.status_code == 200
        assert response.data['id'] == self.user.id
        assert response.data['title'] == 'new title'

        member = User.objects.filter(id=response.data['id']).first()
        assert member.title == response.data['title']

        response = _client(
            self,
            path=f'/apiv1/members/0/',
            method='PUT',
            data=dict(
                title='new title',
                first_name='member first name',
                last_name='member last name',
                email='member@example.com',
                password='123456',
            ),
        )
        assert response.status_code == 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User not found')


