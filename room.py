# Define the Room class.

class Room:
    """
    This class represent a room. A room is composed of a name, a description and exits.

    Attributes :
        name(str) =  a name
        description(str) = a description
        exits(dict) = {}

    Methods :
        __init__(self, name, description): the constructor
        get_exit(self, direction) : the get_exit method
        get_exit_string(self): Return a string describing the room's exits
        get_long_description(self): Return a long description of this room including exits

    Examples (doctest):
        >>> r1 = Room("Forest", "dans une forêt enchantée. Vous entendez une brise légère à travers la cime des arbres.")
        >>> r2 = Room("Tower", "dans une immense tour en pierre qui s'élève au dessus des nuages.")
        >>> r1.exits['E'] = r2
        >>> r1.get_exit('E') is r2
        True
        >>> r1.get_exit('O') is None
        True
        >>> 'Sorties: E' in r1.get_long_description()
        True
    """
    
    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
