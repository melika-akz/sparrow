import pytest
from rest_framework import status

from authorize.models import Member
from .helpers import BaseTestCase


class TestMember(BaseTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.member = Member.objects.create(
            title='member',
            first_name='member first name',
            last_name='member last name',
            email='member@example.com',
            password='123456',
        )

    def test_update(self):
        self.login(self.member)
        response = self._client(
            'Tring to update a member',
            path=f'/apiv1/members/{self.member.id}/',
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
        assert response.data['id'] == self.member.id
        assert response.data['title'] == 'new title'

        member = Member.objects.filter(id=response.data['id']).first()
        assert member.title == response.data['title']

        response = self._client(
            'Trying to update not found member',
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
        self.assertEqual(response.data['detail'], 'Member not found')

        self.logout()
        response = self._client(
            'Unauthorize request',
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