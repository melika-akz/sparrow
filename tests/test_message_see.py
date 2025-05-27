import pytest

from apis.constants import DIRECT
from apis.models import RoomMember, Room, Message
from authorize.models import Member

from .helpers import BaseTestCase, WebSocketTestHelper


class TestMessage(BaseTestCase):

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

        cls.direct1 = Room.objects.create(
            name='direct 1',
            type=DIRECT,
        )

        RoomMember.objects.create(
            room=cls.direct1,
            member=cls.member
        )
        RoomMember.objects.create(
            room=cls.direct1,
            member=cls.member2
        )

        cls.direct2 = Room.objects.create(
            name='direct 2',
            type=DIRECT,
        )

        RoomMember.objects.create(
            room=cls.direct2,
            member=cls.member2
        )
        RoomMember.objects.create(
            room=cls.direct2,
            member=cls.member3
        )

        cls.message1 = Message.objects.create(
            body='this is a message',
            sender=cls.member,
            room=cls.direct1,
        )
        cls.message2 = Message.objects.create(
            body='this is a message2',
            sender=cls.member3,
            room=cls.direct1,
        )

    def test_list(self):
        self.login(self.member)
        ws_helper = WebSocketTestHelper(self.direct1.id)
        assert ws_helper.connect()

        response = self._client(
            'Trying to seen a message',
            path=f'/sparrow/apiv1/messages/{self.message2.id}/',
            method='PATCH',
        )
        assert response.status_code == 200
        assert response.data['body'] == self.message2.body
        assert response.data['sender_id'] == self.member3.id
        assert response.data['seen_at'] is not None
        assert response.data['seen_by'] is not None

        ws_response = ws_helper.receive_json()
        assert ws_response['action'] == 'seen'
        assert ws_response['message']['body'] == 'this is a message2'

        response = self._client(
            'Trying to seen your own message',
            path=f'/sparrow/apiv1/messages/{self.message1.id}/',
            method='PATCH',
        )
        assert response.status_code == 400
        assert response.data['error'] == 'You cannot mark your own message as seen'

