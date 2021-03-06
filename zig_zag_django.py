from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(title="A Generic Room",
                        description="This is a generic room.", x=x, y=y)
            room.save()
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connectRooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 5
width = 3
height = 3
w.generate_rooms(width, height, num_rooms)
w.print_rooms()

print(w.grid)


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")

# Room.objects.all().delete()

# for row in w.grid:
#     for r in row:
#         room = Room(title=r.name, description=r.description, w_id=r.id)
#         room.save()

# for row in w.grid:
#     for r in row:
#         room = Room.objects.get(w_id=r.id)

#         if r.n_to:
#             dest = Room.objects.get(w_id=r.n_to.id)
#             room.connectRooms(dest, "n")

#         if r.s_to:
#             dest = Room.objects.get(w_id=r.s_to.id)
#             room.connectRooms(dest, "s")

#         if r.e_to:
#             dest = Room.objects.get(w_id=r.e_to.id)
#             room.connectRooms(dest, "e")

#         if r.w_to:
#             dest = Room.objects.get(w_id=r.w_to.id)
#             room.connectRooms(dest, "w")
