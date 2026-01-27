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

from debug import DEBUG, debug_print
from quest import QuestManager


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
        
        debug_print(f"Exécution de 'go' avec paramètres: {list_of_words}")

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]

            if DEBUG:  # Vous pouvez aussi utiliser la variable directement
                print(f"DEBUG - Nombre de paramètres: {l}, attendu: {number_of_parameters + 1}")

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
        
        if DEBUG:
            print(f"DEBUG - Direction choisie: {direction}")

        # Move the player in the direction specified by the parameter.
        player.move(direction)

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

        debug_print(f"Exécution de 'take' avec paramètres: {list_of_words}")

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        #code
        player = game.player
        current_room = player.current_room
        name_objet = list_of_words[1] 

        debug_print(f"Tentative de prise de l'objet: {name_objet}")
        
        if name_objet in current_room.inventory:

            objet = current_room.inventory[name_objet]
            weight = player.get_total_weight() + objet.weight

            if name_objet == "locked_desk":
                print(f"\nLe bureau est beaucoup trop lourd pour être déplacé.\n")
                return False
            
            if name_objet == "newspaper":
                player.quest_manager.complete_objective("Prendre newspaper")
            if name_objet == "frame":
                player.quest_manager.complete_objective("Prendre frame")
            if name_objet == "letter":
                player.quest_manager.complete_objective("Prendre letter")

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
    
    def talk(game, list_of_words, number_of_parameters) :
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
    
        # Récupérer le nom du personnage
        character_name = list_of_words[1]
        current_room = game.player.current_room
        player = game.player
        
        # Vérifier si le personnage est dans la pièce
        if character_name not in current_room.character:
            print(f"\n{character_name} n'est pas dans cette pièce.\n")
            return False
        
        # Récupérer le personnage
        character = current_room.character[character_name]
        
        # Obtenir le message
        msg = character.get_msg()

        if character_name == "Doll" :
            player.quest_manager.complete_objective("Parler à Doll")
        
        if msg:
            print(f"\n{character.name} dit : \"{msg}\"\n")
        else:
            print(f"\n{character.name} n'a plus rien à dire...\n")

        
        
        return True
    
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False

    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True


    def use(game, list_of_words, number_of_parameters):
        """
        Utilise un objet de l'inventaire.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        
        Examples:
            >>> use(game, ["use", "flashlight"], 1)
            True
            >>> use(game, ["use"], 1)
            False
        """
        debug_print(f"Exécution de 'use' avec paramètres: {list_of_words}")
        
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        item_name = list_of_words[1]
        
        # Vérifier si l'objet est dans l'inventaire du joueur
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans votre inventaire.\n")
            return False
        
        # Récupérer l'objet
        item_obj = player.inventory[item_name]
        
        # Utiliser l'objet
        success, result_message = item_obj.use(player, player.current_room)

        if result_message:
            print(result_message)
        
        if success:
            #print(result_message)
            
            # Si l'objet est consumable, le retirer après utilisation
            if item_obj.used and hasattr(item_obj, 'consumable') and item_obj.consumable:
                del player.inventory[item_name]
                print(f"{item_name} a été consommé.\n")
            
            # Mettre à jour le poids de l'inventaire
            player.current_weight = player.get_total_weight()
            print(f"Poids de l'inventaire : {player.current_weight}/{player.max_weight}")
            
            # Vérifier les quêtes liées à l'utilisation d'objets
            if hasattr(player, 'quest_manager'):
                player.quest_manager.check_action_objectives("utiliser", item_name)
        
        return success
    