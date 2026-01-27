import random
from debug import debug_print

class Character() :

    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs

    def __str__(self):
        return f"{self.name} : {self.description}"
    
    def move(self):
        change_room = [True, False]
        if random.choice(change_room):
            # Si le personnage est dans une pièce verrouillée, il ne peut pas en sortir
            if hasattr(self.current_room, 'is_locked') and self.current_room.is_locked:
                debug_print(f"{self.name} est enfermé dans {self.current_room.name}")
                return False
            
            # Récupérer toutes les sorties valides (non None)
            possibilities = []
            for direction, room in self.current_room.exits.items():
                if room is not None:
                    # Vérifier que la pièce de destination n'est pas verrouillée
                    if not hasattr(room, 'is_locked') or not room.is_locked:
                        possibilities.append(room)
            
            if possibilities:
                # Choisir une pièce au hasard
                next_room = random.choice(possibilities)

                if self.name in self.current_room.character:
                    del self.current_room.character[self.name]

                debug_print(f"{self.name} se déplace vers {next_room.name}")
                self.current_room = next_room

                self.current_room.character[self.name] = self

                return True
            else:
                debug_print(f"{self.name} n'a aucune sortie disponible")
                return False
        else:
            debug_print(f"{self.name} décide de ne pas bouger")
            return False
    def get_msg(self):
        """
        Retourne et supprime le premier message de la liste.
        Retourne None s'il n'y a plus de messages.
        """
        if not self.msgs:
            return None
    
        # Récupérer le premier message
        msg = self.msgs[0]
        
        # Faire tourner la liste (mettre le premier à la fin)
        self.msgs.append(self.msgs.pop(0))

        return msg