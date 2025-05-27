import pytest
from rest_framework import status

from authorize.models import Member
from .helpers import BaseTestCase


class TestMember(BaseTestCase):

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
        self.login(self.member)
        response = self._client(
            'Trying to get a Member',
            path=f'/apiv1/members/{self.member.id}/',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['id'] == self.member.id

        response = self._client(
            'Trying to get not found user',
            path=f'/apiv1/members/0/',
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

