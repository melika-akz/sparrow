import pytest
from rest_framework import status

from authorize.models import Member
from .helpers import BaseTestCase


class TestSelf(BaseTestCase):

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

    def test_get_self(self):
        self.login(self.member)
        response = self._client(
            'Trying to get self user details',
            path='/apiv1/self/',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['id'] == self.member.id
        assert response.data['title'] == self.member.title
        assert response.data['email'] == self.member.email
        assert response.data['first_name'] == self.member.first_name
        assert response.data['last_name'] == self.member.last_name
        assert response.data['full_name'] == self.member.full_name()
        assert response.data['is_admin'] == self.member.is_admin
        assert response.data['is_staff'] == self.member.is_staff
        assert response.data['is_system'] == self.member.is_system
        assert 'date_joined' in response.data
        assert 'modified_at' in response.data

    def test_get_self_different_user(self):
        self.login(self.member)
        response = self._client(
            'Trying to get self user details',
            path='/apiv1/self/',
            method='GET',
        )
        assert response.data['id'] == self.member.id

        self.logout()
        self.login(self.member2)
        response = self._client(
            'Trying to get self user details for different user',
            path='/apiv1/self/',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['id'] == self.member2.id
        assert response.data['id'] != self.member.id
        assert response.data['email'] == self.member2.email

    def test_get_self_unauthorized(self):
        self.logout()
        response = self._client(
            'Unauthorized request to get self',
            path='/apiv1/self/',
            method='GET',
        )
        assert response.status_code == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

