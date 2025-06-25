from rest_framework.exceptions import ValidationError

from authorize.entities import MemberRepository
from ..models import RoomMember, Room


class RoomMemberFacade:

    def __init__(self, room, member):
        self.room = room
        self.member = member

    def operation_join(self):
        if not RoomMember.objects.filter(room=self.room, member=self.member).exists():
            self.room.add_member(self.member)

    # todo: if created by member leave what happens to the room?
    def operation_leave(self):
        if RoomMember.objects.filter(room=self.room, member=self.member).exists():
            self.room.remove_member(self.member)
        else:
            raise ValidationError("Member is not part of the room")

    def operation_add(self, members):
        if self.room.created_by != self.member:
            raise ValidationError("Only the creator can add members to the room")

        if not members:
            raise ValidationError("No members provided to add")

        for member_id in members:
            member = MemberRepository.get_by_id(member_id)
            self.room.add_member(member)

    def operation_remove(self, members):
        if self.room.created_by != self.member:
            raise ValidationError("Only the creator can remove members from the room")
        if not members:
            raise ValidationError("No members provided to remove")

        for member_id in members:
            member = MemberRepository.get_by_id(member_id)
            self.room.remove_member(member)
