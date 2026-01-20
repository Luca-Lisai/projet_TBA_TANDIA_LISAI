# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import item


class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []
        self.inventory = {}

    # Setup the game
    def setup(self):
 
        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " affiche l'historique du joueur", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : affiche les items de la pièce", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " : prend un objet de la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " : déposer un objet dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : affiche l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check

        # Setup rooms

        entry = Room("Entry", "l'entrée, son couloir très étroit et ses vieux meubles rendent difficile les deplacements.")
        self.rooms.append(entry)
        kitchen = Room("Kitchen", "la cuisine, certains placards sont encore ouverts, remplis de rats et sens dessus dessous, est-ce normal ?")
        self.rooms.append(kitchen)
        living_room = Room("Living_room", "le salon, ces meubles à moitié vide, sa vieille télé éteinte et son fauteil avec une tâche... rouge !")
        self.rooms.append(living_room)
        dining_room = Room("Dining_room", "la salle à manger, la table semble à moitié mise et sa vaisselle plus que délabré.")
        self.rooms.append(dining_room)
        bedroom_1 = Room("Bedroom_1", "une chambre qui semble être celle d'un couple mariés. Les cadres des photos sont tous brisés." )
        self.rooms.append(bedroom_1)
        bedroom_2 = Room("Bedroom_2", "une chambre qui semble être celles d'enfants. Leurs jouets sont dispersés d'une manière pour le moins.. étrange.")
        self.rooms.append(bedroom_2)
        bathroom = Room("Bathroom", "la salle de bain, la baignoire est remplie d'une eau sale, et le miroir fissuré.")
        self.rooms.append(bathroom)
        office = Room("Office", "le bureau, ses meubles en bois massifs ornés de sculptures, et son miroir taille humaine avec trois têtes d'anges en son sommet rendent la poèce lugubre.")
        self.rooms.append(office)
        cave = Room("Cave", "une cave profonde et sombre. Une voix semblent provenir du fond de la salle.")
        self.rooms.append(cave)

        # Create exits for rooms

        entry.exits = {"N" : kitchen, "E" : None, "O" : living_room, "S" : None, "U" : office, "D" : cave}
        kitchen.exits = {"N" : None, "E" : None, "O" : dining_room, "S" : entry, "U" : None, "D" : None}
        living_room.exits = {"N" : dining_room, "E" : entry, "O" : None, "S" : None, "U" : None, "D" : None}
        dining_room.exits = {"N" : None, "E" : kitchen, "O" : None, "S" : living_room, "U" : None, "D" : None}
        bedroom_1.exits = {"N" : office, "E" : bathroom, "O" : None, "S" : None, "U" : None, "D" : None}
        bedroom_2.exits = {"N" : None, "E" : None, "O" : office, "S" : bathroom, "U" : None, "D" : None}
        bathroom.exits = {"N" : bedroom_2, "E" : None, "O" : bedroom_1, "S" : None, "U" : None, "D" : None}
        office.exits = {"N" : None, "E" : bedroom_2, "O" : None, "S" : bedroom_1, "U" : None, "D" : entry}
        cave.exits = {"N" : None, "E" : None, "O" : None, "S" : None, "U" : entry, "D" : None}

        #Create items for rooms
        bedroom_1.inventory = {"flashlight": item("flashlight", "vieille lampe torche éclairant faiblement la zone ",1)}
        self.inventory["flashlight"] = bedroom_1.inventory["flashlight"]

        bathroom.inventory = {"screwdriver": item("screwdriver", "Tournevis à tête plate ", 0.5)}
        self.inventory["screwdriver"] = bathroom.inventory["screwdriver"]
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = entry

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is empty, print nothing
        if not command_string.strip() :
            return

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)
            

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())


def main():
    # Create a game object and play the game
    Game().play()


if __name__ == "__main__":
    main()
