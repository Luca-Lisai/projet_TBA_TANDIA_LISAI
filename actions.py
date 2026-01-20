# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        directions_possibles = {'N', 'S', 'E', 'O', 'U', 'D'}
        direction = list_of_words[1]

        match direction.upper():
            case "N" | "NORD" :
                direction = "N"
            case "S" | "SUD" :
                direction = "S"
            case "E" | "EST" :
                direction = "E"
            case "O" | "OUEST" :
                direction = "O"
            case "U" | "UP" :
                direction = "U"
            case "D" | "DOWN" :
                direction = "D"


        if direction not in directions_possibles :
            print(f"\nLa direction '{direction}' n'est pas reconnue, veuillez en saisir une valide.")
            return False

        # Move the player in the direction specified by the parameter.
        player.move(direction)

        history_text = player.get_history()
        if history_text :
            print(history_text)

        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    def history(game, list_of_words, number_of_parameters) :
        if len(list_of_words)!= 1:#"history" sans paramètre
            print(MSG0.format(command_word="history"))
            return False
        print(game.player.get_history())# Affiche l'historique du joueur
        return True

    def back(game, list_of_words, number_of_parameters) :

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player

        # Impossible de revenir en arrière s'il n'y a qu'une seule pièce
        if len(player.history) <= 1:
            print("\nVous ne pouvez pas revenir en arrière.\n")
            return False

        # Revenir à la pièce précédente
        previous_room = player.history[-1]
        player.current_room = previous_room

        # Retire la pièce actuelle
        player.history.pop()

        print(f"\n{previous_room.get_long_description()}\n" + f"{player.get_history()}\n")

        return True

    def look(game, list_of_words, number_of_parameters) :
        if len(list_of_words)!= 1:#"look" sans paramètre
            print(MSG0.format(command_word="look"))
            return False
        print(game.player.current_room.get_inventory())# Affiche les items dans la piece
        return True
    
    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        #code
        player = game.player
        current_room = player.current_room
        name_objet = list_of_words[1] 
        

        if name_objet in current_room.inventory:

            objet = current_room.inventory[name_objet]
            weight = player.get_total_weight() + objet.weight

            if weight > player.max_weight :
                print(f"Inventaire trop lourd.\n")
            else :
                player.current_weight = weight                                
                objet = current_room.inventory[name_objet]
                player.inventory[name_objet] = objet
                del current_room.inventory[name_objet]
                print(f"L'objet {name_objet} est dans votre inventaire.\n")  # f-string ajouté
        else:
            print(f"L'objet {name_objet} n'est pas dans cette pièce.\n")  # f-string ajouté
        print(f"Poids de l'inventaire : {player.current_weight}/{player.max_weight}")
        return True
    
    def drop(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
                command_word = list_of_words[0]
                print(MSG1.format(command_word=command_word))
                return False
        
        #code
        player = game.player
        current_room = player.current_room
        name_objet = list_of_words[1]
    
        if name_objet in player.inventory:
            objet = player.inventory[name_objet]
            current_room.inventory[name_objet] = objet
            del player.inventory[name_objet]
            print(f"L'objet {name_objet} a été déposé dans la pièce.\n")
        else:
            print(f"L'objet {name_objet} n'est pas dans votre inventaire.\n")
        return True 
    
    def check(game, list_of_words, number_of_parameters) :
        l = len(list_of_words)
        if l != number_of_parameters + 1:
                command_word = list_of_words[0]
                print(MSG0.format(command_word=command_word))
                return False
        print(game.player.get_inventory())
        return True