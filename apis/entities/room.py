from ..models import Room, RoomMember


class RoomRepository:

    @staticmethod
    def check_exist_direct_room(destination_id, source_id):
        source_rooms = RoomMember.objects.filter(member_id=source_id).values_list('room_id', flat=True)
        destination_rooms = RoomMember.objects.filter(member_id=destination_id).values_list('room_id', flat=True)

        common_room_ids = set(source_rooms).intersection(set(destination_rooms))
        if common_room_ids:
            return Room.objects.filter(id__in=common_room_ids).first()

        return None

    @staticmethod
    def check_exist_room(name, type_):
        room = Room.objects.filter(name=name, type=type_).first()
        return room

    @staticmethod
    def get_by_id(room_id):
        room = Room.objects.get(pk=room_id)
        return room
