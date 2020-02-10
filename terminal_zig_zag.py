from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

grid = [None] * 10
width = 10
height = 10
for i in range(len(grid)):
    grid[i] = [None] * 10

x = -1
y = 0
room_count = 0

direction = 1

previous_room = None
while room_count < 100:

    if direction > 0 and x < 10 - 1:
        room_direction = "e"
        room_rev_dir = "w"
        x += 1
    elif direction < 0 and x > 0:
        room_direction = "w"
        room_rev_dir = "e"
        x -= 1
    else:
        room_direction = "n"
        room_rev_dir = "s"
        y += 1
        direction *= -1

    room = Room(title="A Generic Room", description="This is a generic room.", x=x, y=y)
    room.save()

    grid[y][x] = room

    if previous_room is not None:
        previous_room.connectRooms(room, room_direction)
        room.connectRooms(previous_room, room_rev_dir)

    previous_room = room
    room_count += 1

players=Player.objects.all()
for p in players:
  p.currentRoom=Room.objects.all()[0].id
  p.save()
