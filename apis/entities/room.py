from ..models import RoomMember, Room


class RoomRepository:

    @staticmethod
    def check_exist_direct_room(destination_id, source_id):
        source_rooms = RoomMember.objects.filter(user_id=source_id).values_list('room_id', flat=True)
        destination_rooms = RoomMember.objects.filter(user_id=destination_id).values_list('room_id', flat=True)

        common_room_ids = set(source_rooms).intersection(set(destination_rooms))
        if common_room_ids:
            return Room.objects.filter(id__in=common_room_ids).first()

        return None

    @staticmethod
    def check_exist_room(name, type_):
        room = Room.objects.filter(name=name, type=type_).first()
        return room

