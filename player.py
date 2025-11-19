# Define the Player class.
class Player():
    """
    This class represents the player.

    Attributes:
        name (str): The player's name.
        current_room (Room | None): The player's current room, or
            `None` if the player is not placed in any room.

    Methods:
        __init__(name): Initialize a player with a name.
        move(direction): Attempts to move the player in the given
            direction; returns `True` if the move succeeded, `False`
            if the exit exists but is `None`.

    Exceptions raised:
        KeyError: If `direction` does not exist in the
            `current_room.exits` dictionary (for example a typo in the
            direction).
        AttributeError: If `current_room` is `None` at the time of the
            call (player has no assigned room).

    Examples (doctest):
        >>> from room import Room
        >>> r1 = Room("Forest", "dans une forêt enchantée. Vous entendez une brise légère à travers la cime des arbres.")
        >>> r2 = Room("Tower", "dans une immense tour en pierre qui s'élève au dessus des nuages.")
        >>> r1.exits['E'] = r2
        >>> r1.exits['N'] = None
        >>> p = Player("Bassirou")
        >>> p.current_room = r1
        >>> p.move('E') is True
        True
        >>> p.current_room is r2
        True
        >>> p.move('N') is False
        True
     """

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    