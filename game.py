# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import item
from character import Character
from debug import DEBUG, debug_print
from item_actions import use_flashlight, use_screwdriver, use_key_on_door, use_detector, use_letter, use_newspaper
from quest import Quest
# Import modules
from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []
        self.inventory = {}
        self.character = {}
        self.first_cave_visit = True

        self.DEBUG = DEBUG

        if DEBUG:
            print("Mode débogage activé")

    # Setup the game
    def setup(self, player_name=None):
 
        if DEBUG:
            print("Début du setup du jeu...")

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
        take = Command("take", " <objet> : prend un objet de la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <objet> : déposer un objet dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : affiche l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " : fait parler le PNJ", Actions.talk, 1)
        self.commands["talk"] = talk
        use_cmd = Command("use", " <objet> : utiliser un objet de votre inventaire", Actions.use, 1)
        self.commands["use"] = use_cmd
        quests = Command("quests", " : affiche les différentes quêtes proposées", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <objet> : affiche les détails de la quête", Actions.quest, 1)
        self.commands["quest"] = quest
        activate = Command("activate", " <objet> : active la quête demandée", Actions.activate, 1)
        self.commands["activate"] = activate
        rewards = Command("rewards", " : affiche les récompenses obtenus lors de l'achévement des divers quêtes.", Actions.rewards, 0)
        self.commands["rewards"] = rewards

        # Setup rooms

        entry = Room("Entry", "l'entrée, son couloir très étroit et ses vieux meubles rendent difficile les deplacements.","entry.png" )
        self.rooms.append(entry)
        kitchen = Room("Kitchen", "la cuisine, certains placards sont encore ouverts, remplis de rats et sens dessus dessous, est-ce normal ?","kitchen.png")
        self.rooms.append(kitchen)
        living_room = Room("Living_room", "le salon, ces meubles à moitié vide, sa vieille télé éteinte et son fauteil avec une tâche... rouge !","living_room.png")
        self.rooms.append(living_room)
        dining_room = Room("Dining_room", "la salle à manger, la table semble à moitié mise et sa vaisselle plus que délabré.","dining_room.png")
        self.rooms.append(dining_room)
        bedroom_1 = Room("Bedroom_1", "une chambre qui semble être celle d'un couple mariés. Les cadres des photos sont tous brisés.","bedroom_1.png" )
        self.rooms.append(bedroom_1)
        bedroom_2 = Room("Bedroom_2", "une chambre qui semble être celles d'enfants. Leurs jouets sont dispersés d'une manière pour le moins.. étrange.","bedroom_2.png")
        self.rooms.append(bedroom_2)
        bathroom = Room("Bathroom", "la salle de bain, la baignoire est remplie d'une eau sale, et le miroir fissuré.","salle_de_bain.png")
        self.rooms.append(bathroom)
        office = Room("Office", "le bureau, ses meubles en bois massifs ornés de sculptures, et son miroir taille humaine avec trois têtes d'anges en son sommet rendent la poèce lugubre.","bureau.png")
        self.rooms.append(office)
        cave = Room("Cave", "une cave profonde et sombre. Une voix semblent provenir du fond de la salle.","cave.png")
        self.rooms.append(cave)
        secret_room = Room("Secret Room", "une chambre secrète. Des étagères remplies de vieux livres poussiéreux...","secret_room.png")
        self.rooms.append(secret_room)

        # Marquer la cave comme verrouillée
        cave.is_locked = True  # Nouvel attribut
        cave.lock_key = "old_key"  # Nom de la clé nécessaire
        cave.lock_description = "Une vieille porte en bois avec une serrure rouillée."
        # Create exits for rooms

        entry.exits = {"N" : kitchen, "E" : None, "O" : living_room, "S" : None, "U" : office, "D" : cave}
        kitchen.exits = {"N" : None, "E" : None, "O" : dining_room, "S" : entry, "U" : None, "D" : None}
        living_room.exits = {"N" : dining_room, "E" : entry, "O" : None, "S" : None, "U" : None, "D" : None}
        dining_room.exits = {"N" : None, "E" : kitchen, "O" : None, "S" : living_room, "U" : None, "D" : None}
        bedroom_1.exits = {"N" : office, "E" : bathroom, "O" : None, "S" : None, "U" : None, "D" : None}
        bedroom_2.exits = {"N" : None, "E" : None, "O" : office, "S" : bathroom, "U" : None, "D" : None}
        bathroom.exits = {"N" : bedroom_2, "E" : None, "O" : bedroom_1, "S" : None, "U" : None, "D" : None}
        office.exits = {"N" : None, "E" : bedroom_2, "O" : None, "S" : bedroom_1, "U" : None, "D" : entry}
        cave.exits = {"N" : secret_room, "E" : None, "O" : None, "S" : None, "U" : entry, "D" : None}
        secret_room.exits = {"N" : None, "E" : None, "O" : None, "S" : cave, "U" : None, "D" : None}
        cave.exits = {"N" : None, "E" : None, "O" : None, "S" : None, "U" : entry, "D" : None}
        secret_room.exits = {"N" : None, "E" : None, "O" : None, "S" : cave, "U" : None, "D" : None}

        # Stocker la référence pour plus tard
        self.secret_room = secret_room
        self.cave = cave

        #Create items for rooms
        bedroom_1.inventory = {
            "flashlight": item(
                "flashlight",
                "vieille lampe torche éclairant faiblement la zone ",
                1,
                use_action=use_flashlight
            ),
            "mirror": item(
                "mirror",
                "Un vieux mirror argenté qui semble avoir des propriétés mystiques",
                1.5,
                use_action=None
            )
        }
        self.inventory["flashlight"] = bedroom_1.inventory["flashlight"]
        self.inventory["mirror"] = bedroom_1.inventory["mirror"]


        bathroom.inventory = {
            "screwdriver": item(
                "screwdriver",
                "Tournevis à tête plate ",
                0.5,
                use_action=use_screwdriver
            )
        }
        self.inventory["screwdriver"] = bathroom.inventory["screwdriver"]

        self.old_key_item = item(
            "old_key",
            "Une vieille clé rouillée qui semble correspondre à une serrure ancienne",
            0.1,
            use_action=use_key_on_door
            )

        office.inventory = {
            "locked_desk": item(
                "locked_desk",
                "Un vieux bureau en bois avec un tiroir qui semble coincé",
                50,
                use_action=None
            )
        }
        self.inventory["locked_desk"] = office.inventory["locked_desk"]

        
        living_room.inventory = {
            "frame": item(
                "frame",
                "Un cadre avec la photo d'une famille semblant soudée, l'enfant semble tenir un jouet rouge et jaune. Il pourrait être une pièce d'un puzzle ",
                1,
                use_action=None
            )
        }
        self.inventory["frame"] = living_room.inventory["frame"]

        dining_room.inventory = {
            "newspaper": item(
                "newspaper",
                "Un journal contenant un gros titre pour le moins accablant. Il pourrait être une pièce d'un puzzle",
                0.7,
                use_action = use_newspaper
            )
        }
        self.inventory["newspaper"] = dining_room.inventory["newspaper"]

        secret_room.inventory = {
            "letter": item(
                "letter",
                "Une lettre remplie d'un lourd secret. Elle pourrait être une pièce d'un puzzle",
                0.7,
                use_action=use_letter
            )
        }
        self.inventory["letter"] = secret_room.inventory["letter"]

        cave.inventory = {
            "detector": item(
                "detector",
                "Un détecteur d'activité paranormale high-tech",
                1.5,
                use_action=use_detector
            )
        }
        self.inventory["detector"] = cave.inventory["detector"]

        #Create characters for rooms
        cave.character = {"Ghost" : Character("Ghost", "Sa large silouhette blanche et son visage remplis de haine vous glace le sang", cave, ["Il ne me laisse pas le choix . . .", "Ce n'est pas ma faute"])}
        self.character["Ghost"] = cave.character["Ghost"]

        bedroom_2.character = {"Doll" : Character("Doll", "Une poupée en porcelaine assise sur le lit. Ses yeux en boutons semblent vous suivre"
                                                    , bedroom_2, ["Maman est très très furieuse, et si tu veux savoir pourquoi, tu devras connaitre notre histoire",
                                                                  "Joue avec moi, ramène moi les clés de mon passé et peut-être tu survivras *rire d'enfant*"])}
        self.character["Doll"] = bedroom_2.character["Doll"]

        if player_name is None:
            # Mode CLI: demander le nom
            player_name_input = input("\nEntrez votre nom: ")
        else:
            # Mode GUI: utiliser le nom fourni
            player_name_input = player_name
        
        self.player = Player(player_name_input, self)  # <-- Utilisez player_name_input
        self.player.current_room = entry

        decouverte_maison = Quest(
            title= "Découverte de la maison",
            description= "Découvrez le premier étage",
            objectives = ["Visiter Office",
                          "Visiter Bathroom",
                          "Visiter Bedroom_1",
                          "Visiter Bedroom_2"], 
            reward= " badge de la bravoure" )
        detective = Quest(
            title = "Détective",
            description="Trouver les 3 objets pour percer le mystère de cette maison",
            objectives=["Prendre newspaper",
                        "Prendre letter",
                        "Prendre frame"],
            reward= "Badge de détective"
        )
        Medium = Quest(
            title="Medium",
            description= "Parle avec la poupée",
            objectives= ["Parler à Doll"],
            reward= "Badge de medium"
        )

        self.player.quest_manager.add_quest(decouverte_maison)
        self.player.quest_manager.add_quest(detective)
        self.player.quest_manager.add_quest(Medium)

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))

        print("\nTapez 'quit' pour quitter le jeu.")
        while True:
            user_input = input("> ").strip().lower()
            if user_input == "quit":
                print(f"\nMerci {self.player.name} d'avoir joué. Au revoir.\n")
                break
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        if DEBUG:
            print(f"Commande reçue: '{command_string}'")
            
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
        print("\nC'est une nuit où l'orage gronde et le tonnerre retentit. " \
        "Il est clair que la tempête est tout proche. Votre voiture ne veut plus démarrer. " \
        "Seule solution, s'abriter dans la maison la plus proche.")
        print("\nVous apercevez non loin un manoir et vous vous y rendez. " \
        "En approchant du manoir, vous remarquez que la lumière du rez-de-chaussée vacille, comme si quelqu'un ou quelque chose passait devant… " \
        "Pourtant, aucune ombre ne se dessine derrière les vitres.")
        print("\nTOC TOC TOC, personne ne répond... " \
        "Pourtant, en vous approchant de la porte, vous pouvez les entendre, ces bruits qui surgissent depuis l'intérieur. " \
        "Vous décidez d'entrer. La poignée de la porte cède sans résistance, comme si on vous attendait. " \
        "Une odeur de cire et de bois humide vous enveloppe, presque réconfortante… " \
        "Jusqu’à ce que la porte se referme derrière vous avec un claquement sec.")
        print("\nUne fois la porte refermée, vous les entendez à nouveau, ces petits bruits, pourtant, impossible de savoir d'où ils proviennent… "\
              "Les bruits ne ressemblent à rien de connu :"\
               " un grattement métallique, un chuchotement étouffé, puis un rire d’enfant… qui s’arrête net quand vous tendez l’oreille.\n")
        #
        print(self.player.current_room.get_long_description())
       


##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_n = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_s = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_o = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_e = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))

        self._btn_u = tk.PhotoImage(file=str(assets_dir / 'btn_up_50.png'))
        self._btn_d = tk.PhotoImage(file=str(assets_dir / 'btn_down_50.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_n,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_o,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_e,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_s,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_u,
                  command=lambda: self._send_command("go U"),
                  bd=0).grid(row=0, column=1, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_d,
                  command=lambda: self._send_command("go D"),
                  bd=0).grid(row=2, column=1, columnspan=2)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=2, column=0, sticky="ew", pady=(8,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Désactiver l'entrée et attendre que l'utilisateur ferme manuellement
            self.entry.configure(state="disabled")
            # Afficher un message pour indiquer que le jeu est terminé
            print("\n" + "="*60)
            print("Le jeu est terminé. Vous pouvez fermer cette fenêtre.")
            print("="*60 + "\n")

    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()


if __name__ == "__main__":
    main()