
def use_flashlight(player, current_room, item_obj):
    """
    Action pour utiliser la lampe torche.
    Dans la cave : révèle un passage secret au nord.
    """
    game = player.game  # Nous devrons ajouter une référence au jeu dans Player
    
    if current_room.name == "Cave":
        # Vérifier si le passage n'a pas déjà été révélé
        if current_room.exits.get("N") is None:
            # Récupérer la salle secrète depuis le jeu
            secret_room = game.secret_room
            
            # Créer la connexion bidirectionnelle
            current_room.exits["N"] = secret_room
            secret_room.exits["S"] = current_room
            
            # Marquer la lampe comme utilisée
            item_obj.used = True
            
            return True, "\n💡 La lampe torche éclaire la cave sombre. " \
                        "Vous voyez maintenant un passage secret au nord !\n"
        else:
            return True, "\n💡 La lampe torche éclaire déjà le passage secret.\n"
    else:
        # Effet normal dans les autres pièces
        return True, "\n💡 Vous allumez la lampe torche, elle éclaire faiblement la pièce.\n"

def use_screwdriver(player, current_room, item_obj):
    """
    Action pour utiliser le tournevis
    """
    if current_room.name == "Office":
        # Vérifier si un objet spécifique est dans la pièce
        if "locked_desk" in current_room.inventory:
            return True, "\n🔧 Vous utilisez le tournevis pour ouvrir le bureau verrouillé. Vous trouvez une clé!\n"
        else:
            return True, "\n🔧 Vous tournez le tournevis dans vos mains, mais il n'y a rien à dévisser ici.\n"
    else:
        return True, "\n🔧 Vous avez le tournevis en main, mais son utilisation ne semble pas nécéssaire ici.\n"


def use_key_on_door(player, current_room, item_obj):
    """
    Utilise une clé pour déverrouiller une porte.
    """
    game = player.game
    
    # Vérifier si le joueur est à l'entrée et essaie d'ouvrir la cave
    if player.current_room.name == "Entry":
        # Trouver la cave
        cave_room = None
        for room in game.rooms:
            if room.name == "Cave":
                cave_room = room
                break
        
        if cave_room and hasattr(cave_room, 'is_locked') and cave_room.is_locked:
            # Vérifier si c'est la bonne clé
            if item_obj.name == getattr(cave_room, 'lock_key', 'old_key'):
                # Déverrouiller la porte
                cave_room.is_locked = False
                
                # Créer la connexion
                current_room.exits["D"] = cave_room
                cave_room.exits["U"] = current_room
                
                # Supprimer la clé de l'inventaire (consommable)
                del player.inventory[item_obj.name]
                
                print("\n" + "="*60)
                print("🔑 LA CLÉ TOURNE DANS LA SERRURE !")
                print("Un clic sonore résonne dans le silence...")
                print("La trappe de la cave s'ouvre lentement.")
                print("La clé se brise en deux suite à cette ouverture...")
                print("="*60 + "\n")                
                return True, ""
            else:
                return False, "\n🔑 Cette clé ne semble pas correspondre à cette serrure.\n"
        else:
            return False, "\n La porte est déja ouverte."
    
    else :
        return False, "\n🔑 Il n'y a aucune porte à déverrouiller ici.\n"
    
def use_detector(player, current_room, item_obj):
    """
    Action pour utiliser le détecteur de fantôme.
    Révèle la position actuelle du fantôme.
    """
    game = player.game
    
    # Vérifier si le fantôme existe dans le jeu
    if "Ghost" in game.character:
        ghost = game.character["Ghost"]
        ghost_room = ghost.current_room
        
        print("\n" + "="*60)
        print("📡 DÉTECTEUR DE FANTÔME ACTIVÉ 📡\n\n")
        print("Des ondes paranormales sont détectées !")
        print(f"\n👻 Le fantôme se trouve actuellement dans : {ghost_room.name}")
        print("="*60 + "\n")
        
        return True, ""
    else:
        return True, "\n📡 Le détecteur ne détecte aucune présence paranormale.\n"
    
def use_letter(player, current_room, item_obj) :
    print(" Cela fait 3 mois qu'on me les a enlevés et je ne peux le supporter plus longtemps." \
    "Voir le jouet qu'il avait lorsque c'est arrivé m'est trop douloureux." \
    "Il est temps que tout cesse, et si je ne peux pas avoir ma vengeance dans cette vie..." \
    "            JE L'AURAIS DANS L'AUTRE !!!          ")
    return True

def use_newspaper(player, current_room, item_obj) :
    print("BIG NEWS : Meurtre chez les Lancaster !" \
    "C'est une terrible nouvelle que nous apprenons là. Alors que cette petite famille reculée vivait paisiblement, " \
    "son destin a été brutalement anéanti un soir de tempête, lorsqu'un homme lui demanda refuge pour la nuit." \
    "L'homme à assassiné le mari et les deux enfants, ne laissant que le jouet d'un enfant ensanglanté." \
    "La femme fut la seule miraculée de ce cauchemar, avec de sévères entorses et contusions." \
    "Nous lui adressons toutes nos condoléances et beaucoup de courage pour les moments qui lui restent à traverser.")
    return True

def use_screwdriver(player, current_room, item_obj):
    """
    Action pour utiliser le tournevis.
    Dans l'office : ouvre le bureau verrouillé et révèle la clé.
    """
    game = player.game
    
    if current_room.name == "Office":
        # Vérifier si le bureau verrouillé est dans la pièce
        if "locked_desk" in current_room.inventory:
            print("\n" + "="*60)
            print("🔧 UTILISATION DU TOURNEVIS 🔧")
            print("="*60)
            print("\nVous insérez le tournevis dans le tiroir coincé...")
            print("Après quelques efforts, vous entendez un *clic* !")
            print("Le tiroir s'ouvre lentement...")
            print("\n🔑 Vous trouvez une vieille clé rouillée à l'intérieur !")
            print("="*60 + "\n")
            
            # Retirer le bureau verrouillé
            del current_room.inventory["locked_desk"]
            
            # Ajouter la clé dans la pièce
            current_room.inventory["old_key"] = game.old_key_item
            
            # Marquer le tournevis comme utilisé (optionnel)
            item_obj.used = True
            
            return True, ""
        else:
            # Le bureau a déjà été ouvert
            return True, "\n🔧 Vous avez déjà ouvert le bureau. Il n'y a rien d'autre à dévisser ici.\n"
    else:
        return True, "\n🔧 Vous avez le tournevis en main, mais rien ne semble nécessiter son utilisation ici.\n"