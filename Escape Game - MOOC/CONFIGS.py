ZONE_PLAN_MINI = (-240, -240)  # Coin inférieur gauche de la zone d'affichage du plan
ZONE_PLAN_MAXI = (50, 200)  # Coin supérieur droit de la zone d'affichage du plan
POINT_AFFICHAGE_ANNONCES = (-240, 240)  # Point d'origine de l'affichage des annonces
POINT_AFFICHAGE_INVENTAIRE = (70, 210)  # Point d'origine de l'affichage de l'inventaire

# Les valeurs ci-dessous définissent les couleurs des cases du plan
COULEUR_CASES = 'white'
COULEUR_COULOIR = 'white'
COULEUR_MUR = 'grey'
COULEUR_OBJECTIF = 'yellow'
COULEUR_PORTE = 'orange'
COULEUR_OBJET = 'green'
COULEUR_VUE = 'wheat'
COULEURS = [COULEUR_COULOIR, COULEUR_MUR, COULEUR_OBJECTIF, COULEUR_PORTE, COULEUR_OBJET, COULEUR_VUE]
COULEUR_EXTERIEUR = 'white'

# Couleur et dimension du personnage
COULEUR_PERSONNAGE = 'red'
RATIO_PERSONNAGE = 0.9  # Rapport entre diamètre du personnage et dimension des cases
POSITION_DEPART = (0, 1)  # Porte d'entrée du château

# Désignation des fichiers de données à utiliser
fichier_plan =  'plan_chateau.txt' #'petit_chateau.txt'
fichier_questions = 'dico_portes.txt'
fichier_objets = 'dico_objets.txt'


"""
Nous supposons donc que la fenêtre turtle est contenue dans un rectangle (de coin inférieur gauche en (-240, -240) et
de coin supérieur droit (240, 240))) et est composée de 3 zones :
 - la zone affichage du plan (de coin inférieur gauche en (-240, -240) et de coin supérieur droit (50, 200)),
 - la zone annonces avec les textes qui seront affichés en (-240, 240) (chaque annonce devra effacer la précédente),
 - la zone affichage de l’inventaire (de coin supérieur gauche en (70, 210) et de coin supérieur droit en (240, 210))
"""
