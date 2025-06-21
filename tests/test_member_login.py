import pytest

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
        cls.member.set_password('123456')
        cls.member.save()

    def test_login(self):
        response = self._client(
            'Trying register new member',
            path='/apiv1/tokens/',
            method='post',
            data=dict(
                email='member@example.com',
                password='123456',
            ),
        )
        assert response.status_code == 200
        assert response.data['access'] is not None

        response = self._client(
            'Trying not existing email',
            path='/apiv1/members/',
            method='post',
            data=dict(
                email='member2@example.com',
                password='123456',
            ),
        )
        assert response.status_code == 400

