from debug import debug_print

class item() :

    def __init__(self, name, description, weight, use_action = None, use_condition = None):
        self.name = name
        self.description = description
        self.weight = weight

        self.use_action = use_action  # Fonction à exécuter lors de l'utilisation
        self.use_condition = use_condition  # Condition pour utiliser l'objet

        self.used = False  # État de l'objet

        debug_print(f"Création de l'objet: {name}")

    def __str__(self):
        return  f"{self.name} : {self.description} ({self.weight} kg)"
    
    
    def use(self, player, current_room):
        """Utilise l'objet"""

        if self.use_action:
            success, result_message = self.use_action(player, current_room, self)
            return success, result_message

        # Action par défaut si aucune action spécifique
        return True, f"Vous utilisez {self.name}, mais rien de particulier ne se produit ."