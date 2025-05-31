import pytest

from messenger.models import Room, Message, RoomMember
from authorize.models import Member
from .helpers import BaseTestCase


class TestUnreadCount(BaseTestCase):

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

        cls.room = Room.objects.create(name='Test Room', type='GROUP')
        cls.room_member = RoomMember.objects.create(
            room=cls.room,
            member=cls.member,
            latest_seen_message=None,
            latest_seen_message_created_at=None
        )
        cls.room_member2 = RoomMember.objects.create(
            room=cls.room,
            member=cls.member2,
            latest_seen_message=None,
            latest_seen_message_created_at=None
        )
        cls.room_member3 = RoomMember.objects.create(
            room=cls.room,
            member=cls.member3,
            latest_seen_message=None,
            latest_seen_message_created_at=None
        )

        cls.room2 = Room.objects.create(name='Test Room2', type='DIRECT')
        cls.room2_member = RoomMember.objects.create(
            room=cls.room2,
            member=cls.member,
            latest_seen_message=None,
            latest_seen_message_created_at=None
        )
        cls.room2_member2 = RoomMember.objects.create(
            room=cls.room2,
            member=cls.member2,
            latest_seen_message=None,
            latest_seen_message_created_at=None
        )

        cls.room3 = Room.objects.create(name='Test Room3', type='CHANNEL')
        cls.room3_member = RoomMember.objects.create(
            room=cls.room3,
            member=cls.member3,
            latest_seen_message=None,
            latest_seen_message_created_at=None
        )

        cls.message1 = Message.objects.create(
            body='Test message 1',
            sender=cls.member2,
            room=cls.room
        )
        cls.message2 = Message.objects.create(
            body='Test message 2',
            sender=cls.member2,
            room=cls.room
        )
        cls.message3 = Message.objects.create(
            body='Test message 3',
            sender=cls.member2,
            room=cls.room2
        )
        cls.message3 = Message.objects.create(
            body='Test message 3',
            sender=cls.member2,
            room=cls.room2
        )

        cls.room_member2.latest_seen_message = cls.message2
        cls.room_member2.latest_seen_message_created_at = cls.message2.created_at
        cls.room_member2.save()

        cls.room_member.latest_seen_message = cls.message1
        cls.room_member.latest_seen_message_created_at = cls.message1.created_at
        cls.room_member.save()


    def test_get_unread_counts_empty(self):
        self.login(self.member)

        response = self._client(
            'Getting unread counts for empty room',
            path='/apiv1/messenger/rooms/unread-counts/',
            method='GET',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 2
        assert response.data['results'][0]['room_type'] == 'DIRECT'
        assert response.data['results'][0]['total_unread'] == 2
        assert response.data['results'][1]['room_type'] == 'GROUP'
        assert response.data['results'][1]['total_unread'] == 1

        self.login(self.member3)
        response = self._client(
            'Getting unread counts for channels and groups room',
            path='/apiv1/messenger/rooms/unread-counts/',
            method='GET',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 2
        assert response.data['results'][0]['room_type'] == 'CHANNEL'
        assert response.data['results'][0]['total_unread'] == 0
        assert response.data['results'][1]['room_type'] == 'GROUP'
        assert response.data['results'][1]['total_unread'] == 2

        self.logout()
        response = self._client(
            'Getting unread counts without authentication',
            path='/apiv1/messenger/rooms/unread-counts/',
            method='GET',
        )
        assert response.status_code == 401

