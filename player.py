
from debug import debug_print
from quest import QuestManager
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
    def __init__(self, name, game = None):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 5
        self.current_weight = 0.00
        self.quest_manager = QuestManager(self)
        self.game = game
        self.move_count = 0
        self.rewards = []  # List to store earned rewards 

    # Define the move method.
    def move(self, direction):
        debug_print(f"Déplacement du joueur {self.name} vers {direction}")
        
        # Compter les déplacements
        self.move_count += 1
        
        # Vérifier les objectifs de déplacement
        if hasattr(self, 'quest_manager'):
            self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)
        
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]
        
        # Si la pièce suivante existe mais est verrouillée
        if next_room and hasattr(next_room, 'is_locked') and next_room.is_locked:
            print(f"\n🔒 {next_room.lock_description}")
            print(f"La porte est verrouillée. Vous avez besoin d'une clé pour l'ouvrir.\n")
            return False
        
        # If the next room is None, print an error message and return False.
        if next_room is None:
            # Vérifier si c'est la cave qui est verrouillée
            if direction == "D" and self.current_room.name == "Entry":
                cave_room = None
                for room in self.game.rooms:
                    if room.name == "Cave":
                        cave_room = room
                        break
                
                if cave_room and hasattr(cave_room, 'is_locked') and cave_room.is_locked:
                    print(f"\n🔒 {cave_room.lock_description}")
                    print(f"La trappe de la cave est verrouillée. Vous avez besoin d'une clé.\n")
                else:
                    print("\nAucune porte dans cette direction !\n")
            else:
                print("\nAucune porte dans cette direction !\n")
            return False
    
        # Set the current room to the next room.
        self.history.append(self.current_room)
        self.current_room = next_room
        
        # Vérifier les quêtes de visite de pièces
        if hasattr(self, 'quest_manager'):
            self.quest_manager.check_room_objectives(self.current_room.name)
        
        is_first_cave_visit = False
        if self.current_room.name == "Cave" and self.game.first_cave_visit:
            is_first_cave_visit = True

            # Message dramatique
            print("\n" + "="*60)
            print("💀 VOUS DESCENDEZ DANS LA CAVE SOMBRE... 💀")
            print("="*60)
            print("\nSoudain, une présence glaciale vous envahit...")
            print("Une silhouette blanche apparaît devant vous !")
            print("C'est un FANTÔME ! Il vous fixe avec des yeux remplis de haine...")
            print("\nEffrayé, le fantôme s'enfuit dans les profondeurs de la maison !")
            print("\nMais cela ne se reproduira pas, il faudrait mieux éviter de la recroiser de si tôt.")
            print("\nVous entendez maintenant, un peu partout, que le fantôme se déplace, errant de pièces en pièces..")
            print("="*60 + "\n")

            
            # Marquer que la première visite a eu lieu
            self.game.first_cave_visit = False
            
            # Forcer le fantôme à se déplacer
            if "Ghost" in self.game.character:
                ghost = self.game.character["Ghost"]
                old_room = ghost.current_room
                
                # Boucle pour forcer le déplacement
                max_attempts = 10
                attempts = 0
                while old_room == ghost.current_room and attempts < max_attempts:
                    ghost.move()
                    attempts += 1
                
                new_room = ghost.current_room
                
                if old_room != new_room:
                    debug_print(f"👻 {ghost.name} s'est enfui de {old_room.name} vers {new_room.name}")
                else:
                    debug_print(f"👻 {ghost.name} n'a pas pu s'enfuir (aucune sortie disponible)")
        else:
            # Description normale de la pièce
            print(self.current_room.get_long_description())

        # Déplacer le fantôme après le déplacement du joueur
        if self.game and "Ghost" in self.game.character:
            ghost = self.game.character["Ghost"]
            old_room = ghost.current_room
            ghost.move()
            new_room = ghost.current_room
            
            # Message de debug pour voir les déplacements
            if old_room != new_room:
                debug_print(f"👻 {ghost.name} s'est déplacé de {old_room.name} vers {new_room.name}")
            else:
                debug_print(f"👻 {ghost.name} est resté dans {old_room.name}")

        if not is_first_cave_visit and "Ghost" in self.current_room.character:
            
            # Vérifier si le joueur a le jouet (fin heureuse du jeu)
            if "toy" in self.inventory:
                print("\n" + "="*60)
                print("✨✨✨ LE FANTÔME APPARAÎT DEVANT VOUS ✨✨✨")
                print("="*60)
                print("\nLe fantôme surgit avec un cri de rage...")
                print("Mais soudain, il aperçoit le jouet dans vos mains.")
                print("\nSes yeux changent... la haine laisse place à la tristesse.")
                print("Des larmes spectrales coulent sur son visage éthéré...")
                print("\n👻 'Son jouet... Le précieux jouet de mon enfant...'")
                print("\nLe fantôme tend une main tremblante vers l'objet.")
                print("Vous lui tendez doucement le jouet d'enfant.")
                print("\n✨ Une lumière dorée enveloppe le fantôme...")
                print("Son visage retrouve la paix, un sourire apparaît.")
                print("\n👻 'Merci... je peux enfin partir... je suis libre...'")
                print("\nLe fantôme disparaît dans une pluie de lumière scintillante.")
                print("La maison semble soudain plus chaleureuse, plus accueillante.")
                print("\n" + "="*60)
                print("🎊🎊🎊 FÉLICITATIONS ! VOUS AVEZ GAGNÉ ! 🎊🎊🎊")
                print("="*60)
                print("\nVous avez libéré l'âme tourmentée du fantôme.")
                print("La maison n'est plus hantée.")
                print(f"\nMerci d'avoir joué, {self.name} !")
                print("="*60 + "\n")
                
                # Terminer le jeu (victoire)
                self.game.finished = True
                return True
            
            # Vérifier si le joueur a le miroir (protection temporaire)
            elif "mirror" in self.inventory:
                print("\n" + "="*60)
                print("👻 LE FANTÔME APPARAÎT DEVANT VOUS ! 👻")
                print("="*60)
                print("\nLe fantôme surgit avec un cri terrifiant !")
                print("Mais soudain... votre miroir brille d'une lumière argentée !")
                print("🪞 Le fantôme voit son reflet et hurle de terreur !")
                print("Il recule, effrayé par sa propre image, et disparaît dans un nuage de brume...")
                print("\n✨ Le miroir se brise en mille morceaux après avoir utilisé toute sa magie.")
                print("Vous êtes sauf... pour cette fois.")
                print("="*60 + "\n")
                
                # Détruire le miroir
                del self.inventory["mirror"]
                
                # Mettre à jour le poids
                self.current_weight = self.get_total_weight()
                print(f"Poids de l'inventaire : {self.current_weight}/{self.max_weight}\n")
                
                # Forcer le fantôme à fuir dans une autre pièce
                ghost = self.game.character["Ghost"]
                old_room = ghost.current_room
                
                # Boucle pour forcer le déplacement
                max_attempts = 10
                attempts = 0
                while old_room == ghost.current_room and attempts < max_attempts:
                    ghost.move()
                    attempts += 1
                
                if old_room != ghost.current_room:
                    debug_print(f"👻 {ghost.name} s'est enfui de {old_room.name} vers {ghost.current_room.name}")
            
            else:
                # Le joueur n'a ni le jouet ni le miroir, il meurt
                print("\n" + "="*60)
                print("💀💀💀 LE FANTÔME VOUS A TROUVÉ ! 💀💀💀")
                print("="*60)
                print("\nLe fantôme surgit devant vous avec un cri terrifiant !")
                print("Ses yeux brillent d'une lueur maléfique...")
                print("Vous sentez une douleur glaciale vous traverser le corps...")
                print("\n💀 VOUS ÊTES MORT... 💀")
                print("="*60 + "\n")
                
                # Terminer le jeu (défaite)
                self.game.finished = True
                return False
            
        if self.current_room.name == "Bedroom_2":
            # Vérifier si le joueur a les 3 objets requis
            has_letter = "letter" in self.inventory
            has_newspaper = "newspaper" in self.inventory
            has_frame = "frame" in self.inventory
            
            # Vérifier si le jouet n'est pas déjà apparu
            toy_already_appeared = "toy" in self.current_room.inventory
            
            if has_letter and has_newspaper and has_frame and not toy_already_appeared:
                
                # Ajouter le jouet dans l'inventaire de la pièce
                from item import item
                self.current_room.inventory["toy"] = item(
                    "toy",
                    "Un vieux jouet d'enfant qui dégage une étrange énergie",
                    0.5,
                    use_action=None
                )


        return True

    def get_history(self) : 
        """Retourne l'historique des déplacements du joueur."""
        if not self.history:
            return "\nAucun déplacement enregistré.\n"

        lines = ["\nVous avez déjà visité les pièces suivantes:"]
       # On exclut la pièce actuelle (dernière de la liste)
        for room in self.history[::-1]:
            lines.append(f"    - {room.description}")

        return "\n".join(lines)
    
    def get_inventory(self):
        if not self.inventory :
            return "\n inventaire vide\n"
        
        lines = ["\n Vous disposez des objets suivants : "]

        for key, item_obj in self.inventory.items():
            lines.append(f"    - {item_obj}")
        return "\n".join(lines) + "\n"
    
    def get_total_weight(self):
        """Calcule le poids total de l'inventaire"""
        total = 0.0
        for item_obj in self.inventory.values():
            total += item_obj.weight
        return total


    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()
