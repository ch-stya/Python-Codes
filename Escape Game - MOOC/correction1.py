"""

Description du projet : escape game sous forme de labyrinthe avec objets à récolter et
des portes à ouvrir en répondant correctement à des questions. Le but est d'atteindre
la sortie. Le joueur n'est pas obligé de collecter tous les objets pour gagner.
Auteurs : Anaïs Degrève, Anastasia Dubois
Date : du 10/11/2022 au 16/11/2022

"""


# importations et paramètres d'affichage
import turtle
from CONFIGS import *
turtle.speed(0)
turtle.tracer(0)


def lire_matrice(fichier):
    """
    Transforme la matrice en liste d'entiers
    Entrée(s): fichier
    Sortie(s): matrice en liste
    fichier est un nom de variable lambda
    """
    f = open(fichier)
    matrice = list()
    for line in f:
        s = line.strip().split()
        int_list = [int(x) for x in s]
        matrice.append(int_list)  # Ajout dans la liste en INT
    return matrice


def calculer_pas(matrice):
    """
    Calcul de la longueur d'une case carrée
    Entrée: matrice
    Sortie(s): la longueur d'un pas
    matrice est un nom de variable lambda
    """
    lines = len(matrice)
    cols = len(matrice[0])
    pas = int(min(h/lines, l/cols))  # calcul d'un pas
    return pas


def coordonnees(case, pas):
    """
    Calcul des coordonnées du coin inférieur gauche en pixels turtle
    Entrée(s): case, pas
    Sortie(s): coordonnées du coin inférieur gauche de n'importe quelle case
    du labyrinthe
    case et pas sont des noms de variables lambdas
    """
    coin_inferieur_gauche = (ZONE_PLAN_MINI[0], ZONE_PLAN_MAXI[1]-pas)  # coordonnées du coin inférieur gauche
    # de la case supérieure gauche
    coin = ((coin_inferieur_gauche[0] + pas * case[0]), (coin_inferieur_gauche[1] - pas * case[1]))  # coordonnées
    # du coin inférieur gauche de n'importe quelle case du labyrinthe
    return coin


def tracer_carre(dimension):
    """
    Trace un carré
    Entrée(s): taille de la case (pas)
    Sortie(s): /
    dimension est un nom de variable lambda
    """
    for cote in range(4):
        turtle.forward(dimension)
        turtle.left(90)
    turtle.hideturtle()


def tracer_case(case, couleur, pas):
    """
    Trace la case que l'on veut de la couleur que l'on veut
    Entrée(s) : case, couleur, pas
    Sortie(s) : /
    case, couleur et pas sont des noms de variables lambdas
    """
    position = coordonnees(case, pas)
    turtle.up()
    turtle.goto(position)
    turtle.down()
    turtle.color(couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()


def afficher_plan(matrice):
    """
    Dessine le plan du chateau
    Entrée(s): matrice
    Sortie(s): /
    matrice est un nom de variable lambda
    """
    lines = len(matrice)  # la longueur de la liste correspond au nombre de ligne
    cols = len(matrice[0])  # la longueu de la "sous liste", contenue dans l'élément 1
    # de la liste matrice correspond au nombre de colonnes
    for x in range(lines):
        for y in range(cols):
            nature_case = matrice [x][y]  # repère le type de case grâce à ses coordonnées (ligne-colonne)
            if nature_case == 0:  # case vide
                tracer_case((y, x), COULEURS[0], pas)
            if nature_case == 1:  # mur
                tracer_case((y, x), COULEURS[1], pas)
            if nature_case == 2:  # sortie/victoire
                tracer_case((y, x), COULEURS[2], pas)
            if nature_case == 3:  # porte
                tracer_case((y, x), COULEURS[3], pas)
            if nature_case == 4:  # objet à collecter
                tracer_case((y, x), COULEURS[4], pas)


def deplacement(mouvement, nouvelle_position):
    """
    Détermine la nouvelle position du joueur après exécution d'un mouvement
    Entrée(s): mouvement, nouvelle_position
    Sortie(s): la nouvelle position du joueur, après mouvement
    mouvement et nouvelle_position sont des noms de variables lambdas
    """
    if mouvement == 'Left':
        nouvelle_position[0] -= 1       # se deplacer d'une case vers la gauche
    if mouvement == 'Right':
        nouvelle_position[0] += 1       # se deplacer d'une case vers la droite
    if mouvement == 'Up':
        nouvelle_position[1] -= 1       # monter d'une case
    if mouvement == "Down":
        nouvelle_position[1] += 1       # descendre d'une case
    return nouvelle_position


def deplacer(matrice, position, mouvement):
    """
    Détermine l'action à effectuer en fonction de la case sur laquelle
    le joueur veut se rendre
    Entrée(s): matrice, position et mouvements
    Sorties(s): la nouvelle position du joueur
    matrice, position et mouvements sont des noms de variables lambdas
    """
    nouvelle_position = []
    position_retournee = []
    for i in range(len(position)):
        nouvelle_position.append(position[i])
    deplacement(mouvement, nouvelle_position)  # appelle la fonction déplacement

    nouvelle_case = matrice[nouvelle_position[1]][nouvelle_position[0]]
    if nouvelle_case == 0:
        position_retournee = nouvelle_position  # changement de case si vide
        tracer_case([position[0]+1, position[1]], COULEUR_VUE, pas)
        # pour le +1 : on a eu un problème de décalage lors du coloriage des positions
        # précédentes du joueur. La position coloriée etait à chaque fois décalée
        # de 1 sur les x. à défaut de comprendre d'où pouvait venir le problème,
        # on y a remédié en mettant un +1
    if nouvelle_case == 1:
        position_retournee = position
    if nouvelle_case == 2:
        position_retournee = position  # la sortie est considérée comme un mur
        annoncer(COULEURS[2], "Bravo, vous avez trouvez la sortie !!")  # mais la victoire est annoncée
    if nouvelle_case == 3:
        poser_question(matrice, nouvelle_position)  # appelle la fonction poser_question définie plus bas
        position_retournee = position  # que le joueur débloque la porte ou pas,il reste sur sa case
    if nouvelle_case == 4:
        ramasser_objet((nouvelle_position[0], nouvelle_position[1]))  # appelle la fct ramasser_objet définie plus bas
        position_retournee = nouvelle_position
        tracer_case([position[0]+1, position[1]], COULEUR_VUE, pas)  # +1 pour pallier à un décalage
    afficher_joueur(position_retournee)
    return position_retournee


def afficher_joueur(nouvelle_position):
    """
    Entrée(s): nouvelle_position
    Sortie(s): /
    nouvelle_position est un nom de variable lambda
    """
    position_joueur = nouvelle_position
    coo = coordonnees(position_joueur, pas)
    centre = [coo[0]+pas/2, coo[1]+pas/2]  # centre d'une case
    turtle.penup()
    turtle.goto(centre)
    turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)


def deplacer_gauche():
    """
    Se déplacer à gauche à l'appui de la touche directionnelle 'gauche'
    Entrée:/
    Sortie:/
    """
    turtle.onkeypress(None, "Left")   # Désactive la touche Left
    global position_joueur  # pour actualiser la position
    position_joueur = deplacer(matrice, position_joueur, "Left")  # traitement associé à la flèche
    # gauche appuyée par le joueur
    turtle.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche


def deplacer_droite():
    """
    Se déplacer à droite à l'appui de la touche directionnelle 'droite'
    Entrée(s): /
    Sortie(s): /
    """
    turtle.onkeypress(None, "Right")
    global position_joueur
    position_joueur = deplacer(matrice, position_joueur, "Right")
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_bas():
    """
    Se déplacer en bas à l'appui de la touche directionnelle 'bas'
    Entrée(s): /
    Sortie(s): /
    """
    turtle.onkeypress(None, "Down")
    global position_joueur
    position_joueur = deplacer(matrice, position_joueur, "Down")
    turtle.onkeypress(deplacer_bas, "Down")


def deplacer_haut():
    """
    Se déplacer en haut à l'appui de la touche directionnelle 'haut'
    Entrée(s): /
    Sortie(s): /
    """
    turtle.onkeypress(None, "Up")
    global position_joueur
    position_joueur = deplacer(matrice, position_joueur, "Up")
    turtle.onkeypress(deplacer_haut, "Up")


def dessiner_inventaire():
    """
    Dessine l'inventaire
    Entrée(s): /
    Sortie(s): /
    """
    longueur_inv = 0.9 * l  # les dimensions du contour de l'inventaire (hauteur et longueur) sont
    # exprimées par rapport à la longueur et la hauteur du labyrinthe, on leur définit un
    # rapport de proportionallité arbitrairement
    hauteur_inv = 0.5 * h
    turtle.color('Black')
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    turtle.down()
    turtle.forward(longueur_inv)
    turtle.right(90)
    turtle.forward(hauteur_inv)
    turtle.right(90)
    turtle.forward(longueur_inv)
    turtle.right(90)
    turtle.forward(hauteur_inv)
    turtle.write("Inventaire", move=False, font=('Arial', 11, 'normal'))
    turtle.hideturtle()


def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    Création d'un ensemble dictionnaire recensant les objets sur base de
    la lecture d'un fichier
    Utilisation d'un tuple constitué des éléments du fichier dico
    Entrée(s) : fichier
    Sortie(s) : dico
    """
    f = open(fichier_des_objets, encoding="UTF-8")
    dico = {}
    for line in f:
        g = line.strip()
        k, v = eval(g)  # l'instruction a, b = eval(line) permet de récupérer une chaîne du type
        # '(x, y), (c1, c2)' de sorte que a=(x, y) de type Tuple et b=(c1, c2) de type Tuple aussi.
        k1 = (k[1], k[0])
        dico[k1] = v
    return dico


def afficher_objet(nom_objet):
    """
    Affiche les indices (objets) dans l'inventaire
    Entrée(s): nom_objet
    Sortie(s): /
    nom_objet est un nom de variable lambda
    """
    espace_lignes = 15  # valeur pour un espacement entre 2 lignes (noms d'objet) dans l'inventaire
    espace_cadre = 10  # valeur pour l'espacement entre le nom des objets dans l'inventaire et le cadre de l'inventaire
    police = 8   # police d'écriture des objets dans l'inventaire

    turtle.penup()
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE[0]+espace_cadre, POINT_AFFICHAGE_INVENTAIRE[1]-len(inventaire)*espace_lignes)
    turtle.color('black')
    turtle.write(nom_objet, move=False, font=("Arial", police, 'normal'))


def ramasser_objet(case):
    """
    Collecte l'indice
    Entrée(s): case
    Sortie(s): /
    case est un nom de variable lambda
    """
    dico = creer_dictionnaire_des_objets('dico_objets.txt')
    indice = dico.get(case)
    inventaire.append(indice)  # ajoute les indices dans une liste
    afficher_objet(indice)  # on affiche les objets dans l'inventaire, lance la fonction afficher_objet
    annoncer(COULEURS[4], "Vous avez trouvé un indice, regardez votre inventaire!")  # lance la fonction annoncer
    matrice[case[1]][case[0]] = 0  # la case objet devient une case vide quand l'objet est collecté
    # car l'objet ne peut être ramassé qu'une fois


def annoncer(couleur, annonce):
    """
    Ecrit les annonces et efface les anciennes
    Entrée(s): couleur, annonce
    Sortie(s): /
    couleur et annonce sont des noms de variables lambdas
    """
    # Avant d'écrire l'annonce, tracer une zone et la remplir de la couleur du fond, ce qui revient à
    # effacer ce qui s'y trouve. La zone comprend celle des annonces et veille à ne pas empiéter sur le
    # labyrinthe ou l'inventaire pour ne pas les effacer.
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.down()
    turtle.color(COULEUR_EXTERIEUR)
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(0.5 * h)
        turtle.right(90)
        turtle.forward(2 * l)
        turtle.right(90)
    turtle.end_fill()

    police = 16  # police d'écriture des annonces
    turtle.penup()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.color(couleur)
    turtle.write(annonce, font=("Arial", police, 'normal'))
    turtle.penup()


def poser_question(matrice, case):
    """
    Pose une question au joueur (quand il veut aller sur une porte)
    La porte s'ouvre si la réponse du joueur est juste (on le lui annonce)
    et reste fermée si la réponse est fausse.
    Entrée(s): /
    Sortie(s):/
    matrice, case sont des noms de variables lambdas
    """
    dico_portes = creer_dictionnaire_des_objets('dico_portes.txt')
    annoncer(COULEUR_PORTE, "Cette porte est fermée.")  # annonce générale quand il veut se déplacer sur une porte
    porte = case[0], case[1]
    question, reponse = dico_portes[porte]
    saisie = turtle.textinput('Question...', question)
    turtle.listen()  # attente d'une action du joueur
    if saisie == reponse:
        matrice[case[1]][case[0]] = 0  # la porte est ouverte, la case porte devient donc une case vide
        annoncer('DarkGreen', "Bonne réponse, la porte s'ouvre!")  # annonce en VERT quand le joueur a juste
    else:
        annoncer('DarkRed', 'Mauvaise réponse, retentez')  # annonce en ROUGE quand le joueur a faux



l = abs(ZONE_PLAN_MINI[0])+abs(ZONE_PLAN_MAXI[0])  # calcul de la longueur du labyrinthe
h = abs(ZONE_PLAN_MINI[1])+abs(ZONE_PLAN_MAXI[1])  # calcul de la hauteur du labyrinthe
matrice = lire_matrice('plan_chateau.txt')
pas = calculer_pas(matrice)
position_joueur = [POSITION_DEPART[1], POSITION_DEPART[0]]  # le 2e élément en x et le 1er en y car
# le dossier CONFIGS donné en (y,x)
inventaire = []

turtle.bgcolor(COULEUR_EXTERIEUR)  # couleur de fond de la fenêtre turtle
afficher_plan(matrice)
dessiner_inventaire()
afficher_joueur(position_joueur)
turtle.listen()
turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()  # Place le programme en position d’attente d’une action du joueur
turtle.done()