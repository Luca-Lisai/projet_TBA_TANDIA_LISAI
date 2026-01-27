# Variable de débogage globale
DEBUG = False  # Mettez à False pour désactiver les messages de débogage

# Fonction pour afficher les messages de débogage
def debug_print(message, end="\n"):
    """Affiche un message uniquement si DEBUG est True"""
    if DEBUG:
        print(f"[DEBUG] {message}", end=end)