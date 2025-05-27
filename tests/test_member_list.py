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

    def test_list(self):
        self.login(self.member)
        response = self._client(
            'Trying to get list of member',
            path=f'/apiv1/members/',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['count'] == 3
        for member in response.data['results']:
            assert member['id'] in [
                self.member.id,
                self.member2.id,
                self.member3.id
            ]

        response = self._client(
            'Trying to filter by firstname',
            path=f'/apiv1/members/?first_name=member 2',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == self.member2.id

        response = self._client(
            'Trying to filter by lastname',
            path=f'/apiv1/members/?last_name=member 3',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == self.member3.id


        response = self._client(
            'Trying to filter by email',
            path=f'/apiv1/members/?email=member3@example.com',
            method='GET',
        )
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == self.member3.id

        response = self._client(
            'Trying to search member with take and skip',
            path=f'/apiv1/members/?search=member&page=2&page_size=1',
            method='GET',
        )
        print(response.data)
        assert response.status_code == 200
        assert response.data['count'] == 3
        assert response.data['total_pages'] == 3
        assert response.data['current_page'] == 2
        assert response.data['next'] is not None
        assert response.data['previous'] is not None
        assert response.data['results'][0]['id'] == self.member2.id

        self.logout()
        response = self._client(
            'Unauthorize request',
            path='/apiv1/members/',
            method='GET',
        )
        assert response.status_code == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

