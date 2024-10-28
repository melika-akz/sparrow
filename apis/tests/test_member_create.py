import json

import pytest
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

    def test_create(self):
        """Creating Member"""
        response = _client(
            self,
            path='/apiv1/members/',
            method='POST',
            data=dict(
                title='member2',
                email='member2@example.com',
                first_name='member 2 first name',
                last_name='member 2 last name',
                password='123456',
            ),
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['title'] == 'member2'

        member = User.objects.filter(id=response.data['id']).first()
        assert member.title == response.data['title']

        response = _client(
            self,
            path='/apiv1/members/',
            method='POST',
            data=dict(
                title='member3',
                first_name='member 3 first name',
                last_name='member 3 last name',
                email='member2@example.com',
                password='123456',
            ),
        )
        assert response.status_code == 400

