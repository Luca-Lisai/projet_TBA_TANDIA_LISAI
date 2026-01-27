README - Le Manoir Hanté

Description :
Le Manoir Hanté est un jeu d'aventure textuel en Python avec interface graphique. Explorez un manoir mystérieux, résolvez des énigmes, interagissez avec des objets et des personnages surnaturels, et accomplissez des quêtes pour percer les secrets d'une famille au destin tragique.

Caractéristiques :
✅ Deux modes : Interface graphique (Tkinter) et mode console (CLI)

✅ 10 pièces détaillées avec images et descriptions uniques

✅ Système d'inventaire avec gestion du poids

✅ PNJ interactifs (Fantôme, Poupée) avec dialogues cycliques

✅ Système de quêtes avec objectifs et récompenses

✅ Objets interactifs avec actions spécifiques

✅ Portes verrouillées nécessitant des clés

✅ Historique des déplacements et retour en arrière

✅ Mode débogage intégré

✅ Mécanique de survie contre le fantôme

Histoire :
C'est une nuit où l'orage gronde et le tonnerre retentit. Votre voiture ne veut plus démarrer. Seule solution, s'abriter dans le manoir le plus proche...

Vous découvrez la terrible histoire de la famille Lancaster, décimée lors d'une nuit de tempête. Votre mission : découvrir la vérité et libérer les âmes tourmentées.

Commandes Disponibles :

Commande	      |   Exemple	          |        Description
help	          |    help	              |          Affiche toutes les commandes
go <direction>    |    go N	              |          Se déplacer (N, E, S, O, U, D)
look	          |    look	              |          Examiner la pièce actuelle
take <objet>	  |    take flashlight	  |          Prendre un objet
drop <objet>	  |    drop key           |          Déposer un objet
use <objet>       |    use flashlight	  |          Utiliser un objet
check	          |    check	          |          Voir l'inventaire
talk <personnage> |    talk Ghost	      |          Parler à un PNJ
quests	          |    quests	          |          Lister les quêtes
quest <nom>       |    quest Détective	  |          Détails d'une quête
activate <quête>  |	   activate Détective |	         Activer une quête
rewards           |    rewards	          |          Voir les récompenses
history           |    history	          |          Historique des déplacements
back	          |    back	              |          Revenir en arrière
quit              |    quit	              |          Quitter le jeu

Quêtes Principales :
🕵️ Détective
Description : Trouver les 3 objets pour percer le mystère

Objectifs :

Prendre newspaper (journal)

Prendre letter (lettre)

Prendre frame (cadre photo)

Récompense : Badge de détective

🏠 Découverte de la maison
Description : Explorer le premier étage

Objectifs :

Visiter Office

Visiter Bathroom

Visiter Bedroom_1

Visiter Bedroom_2

Récompense : Badge de la bravoure

🔮 Medium
Description : Communiquer avec les esprits

Objectifs :

Parler à Doll (poupée)

Récompense : Badge de medium

Gameplay :
Mécaniques Clés :
Poids de l'inventaire (5kg max) - gérez vos objets !

Fantôme errant - se déplace aléatoirement dans le manoir

Objets spéciaux :

Lampe torche : révèle les passages secrets

Miroir : protège contre le fantôme (une fois)

Tournevis : ouvre le bureau verrouillé

Clé : ouvre la cave

Détecteur : localise le fantôme


Scénarios de Fin :
Fin heureuse : Trouver le jouet d'enfant et le donner au fantôme

Fin tragique : Rencontrer le fantôme sans protection

Fin de survie : Utiliser le miroir pour se protéger


Objets Importants :
Objet	    |  Localisation	|  Utilisation
flashlight	|   Bedroom_1	|    Éclaire la cave, révèle passage secret
mirror	    |   Bedroom_1	|    Protège contre le fantôme (consommable)
screwdriver	|   Bathroom    | 	Ouvre le bureau dans l'Office
old_key	    |   Bureau      |    (après ouverture)	Ouvre la cave
newspaper	|   Dining_room	|    Pièce du puzzle (histoire)
letter	    |   Secret Room	|    Pièce du puzzle (motivation)
frame	    |   Living_room	|    Pièce du puzzle (photo familiale)
detector	|   Cave	    |    Localise le fantôme
toy	        |    Bedroom_2	|    Permet la fin heureuse

 Interface Graphique :
L'interface Tkinter propose :

Zone image (600x400) : affiche l'image de la pièce actuelle

Boutons directionnels : déplacements rapides

Terminal texte : sortie du jeu avec scroll

Champ de commande : saisie des commandes

Boutons d'action : help, quit

Guide du développeur :
![alt text](<Quest Management Framework-2026-01-27-202639.png>)