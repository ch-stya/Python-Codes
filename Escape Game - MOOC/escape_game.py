"""
Chloe QUEHAN
12/11/2022
Petit jeu de type escape game. Le but étant d'atteindre la case jaune 'OBJECTIF'. Possibilité de ramasser des objets (cases
vertes) contenant des indices, possibilité d'ouvrir des portes (cases oranges) en répondant juste à la question posée.
Déplacements avec les flèches du clavier.
"""

from CONFIGS import *
import turtle
turtle.tracer(0) #permet de tracer le plan directement
turtle.speed(0) #vitesse du dessin
turtle.hideturtle() #cache le pinceau

#variables
inventaire = set() #création de l'inventaire
increment_inventaire = 80 #incrément servant à afficher l'inventaire correctement

def lire_matrice(matrice):
    """
    Fonction permettant de lire un plan (fichier txt) et de le renvoyer sous forme de matrice.
    Entrée : Fichier txt contenant des nb entiers séparés par des espaces
    Sortie : Liste de listes (matrice)
    """
    plan = []
    with open(matrice, encoding="utf-8") as matrice :
        for ligne in matrice :
            ligne = ligne.split()
            plan.extend([ligne])
    return plan

def calculer_pas(matrice):
    """
    Fonction permettant de calculer la largeur idéale d'une case en fonction de l'espace
    reservé au plan dans la fenêtre
    Entrée : Matrice(list) du plan
    Sortie : Largeur(int) d'une case (carré)
    """
    hauteur_plan = abs(ZONE_PLAN_MINI[1]-ZONE_PLAN_MAXI[1])
    largeur_plan = abs(ZONE_PLAN_MINI[0]-ZONE_PLAN_MAXI[0])
    cases_hauteur = len(matrice)
    cases_largeur = len(matrice[0])
    dimension_hauteur = hauteur_plan // cases_hauteur
    dimension_largeur = largeur_plan // cases_largeur
    largeur_case = min(dimension_hauteur, dimension_largeur)
    return largeur_case

def coordonnees(case, pas):
    """
    Fonction permettant de retourner l'emplacement d'une case. Créer un dictionnaire répertoriant
    l'emplacement de chaque case en fonction du plan donné et de la largeur de case donné.
    Entrée : Tuple ordonnée, abscisse (y, x) dont on souhaite les coordonnées turtle + largeur d'une case
    Sortie : Couple(tuple) coordonnées turtle
    """
    cases_hauteur = len(matrice)
    cases_largeur = len(matrice[0])
    d = {}
    inc = ZONE_PLAN_MINI
    for i in range(cases_hauteur-1, -1, -1) :
        for j in range(cases_largeur) :
            d[(i, j)] = inc
            inc = tuple(map(lambda l, k: l + k, inc, (pas,0)))
        inc = (ZONE_PLAN_MINI[0], inc[1])
        inc = tuple(map(lambda l, k: l + k, inc, (0,pas)))
    return d[case]

def tracer_carre(dimension):
    """
    Fonction traçant un carré
    Entrée : Dimension(int) souhaitée pour la taille du carré
    """
    turtle.down()
    for i in range(4):
        angle = 90
        turtle.forward(dimension)
        turtle.right(angle)
    return None

def tracer_case(case, couleur, pas):
    """
    Fonction permettant de choisir emplacement, couleur, et taille du carré qu'on va tracer en appelant
    la fonction tracer_carre.
    Entrée : Couple(tuple) avec les coordonnées turtle, couleur(str), largeur du carré(int)
    """
    turtle.up()
    turtle.goto(case)
    turtle.color(couleur)
    turtle.begin_fill()
    turtle.down()
    tracer_carre(pas)
    turtle.end_fill()
    return None

def afficher_plan(matrice):
    """
    Fonction visant à dessiner le plan complet en faisant appel à différentes fonctions.
    Entrée : Matrice(list) du plan
    """
    for i in range(len(matrice)) :
        for j in range(len(matrice[i])) :
            p = matrice[i][j] 
            if p == '0' :
                tracer_case(coordonnees((i,j), largeur_case), COULEUR_CASES, largeur_case)
            elif p == '1' :
                tracer_case(coordonnees((i,j), largeur_case), COULEUR_MUR, largeur_case)
            elif p == '2' :
                tracer_case(coordonnees((i,j), largeur_case), COULEUR_OBJECTIF, largeur_case)
            elif p == '3' :
                tracer_case(coordonnees((i,j), largeur_case), COULEUR_PORTE, largeur_case)
            elif p == '4' :
                tracer_case(coordonnees((i,j), largeur_case), COULEUR_OBJET, largeur_case)
    return None

def tracer_rectangle(dimension):
    """
    Fonction traçant un rectangle blanc.
    Entrée : Dimension(tuple)(largeur, hauteur) souhaitée pour la taille du rectangle
    """
    turtle.up()
    turtle.color('white')
    turtle.down()
    turtle.begin_fill()
    for i in range(2):
        angle = 90
        turtle.forward(dimension[0])
        turtle.right(angle)
        turtle.forward(dimension[1])
        turtle.right(angle)
    turtle.end_fill()
    turtle.up()
    return None

def ecriture_annonce(valeur):
    """
    Fonction permettant d'afficher une annonce
    Entrée : Liste de ce qu'il faut afficher 
    """
    turtle.up()
    turtle.goto(tuple(map(lambda l, k: l + k, POINT_AFFICHAGE_ANNONCES, (-30, 60))))
    tracer_rectangle((600, 100)) #trace un rectangle blanc afin d'effacer ce qui a pu être écrit auparavant
    turtle.color('black')
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    for i in valeur :
        turtle.write(i, True, font=('Arial', 12, 'bold'))
    return None
    
def ecriture_inventaire(valeur):
    """
    Fonction permettant d'écrire dans l'inventaire.
    Entrée : Valeur de l'objet à afficher
    """
    global increment_inventaire
    turtle.up()
    if increment_inventaire < 90 : #la première fois (pour écrire "Inventaire :")
        turtle.goto(tuple(map(lambda l, k: l - k, POINT_AFFICHAGE_INVENTAIRE, (-40, increment_inventaire))))
        turtle.color('black')
        turtle.write(valeur, True, font=('Arial', 11, 'bold'))
        increment_inventaire = increment_inventaire + 40
    elif increment_inventaire > 90 : #ensuite ce sera sous la forme d'une liste
        turtle.goto(tuple(map(lambda l, k: l - k, POINT_AFFICHAGE_INVENTAIRE, (-20, increment_inventaire))))
        turtle.color('black')
        turtle.write(' -   ', True, font=('Arial', 10, 'normal'))
        turtle.write(valeur, True, font=('Arial', 10, 'normal'))
        increment_inventaire = increment_inventaire + 30
    return None

def deplacer_gauche():
    """
    Fonction permettant de se déplacer vers la gauche (appel de la fonction deplacer).
    """
    global matrice, position_act
    turtle.onkeypress(None, "Left")   # Désactive la touche Left
    new_position = tuple(map(lambda l, k: l + k, position_act, (0, -1)))
    deplacer(matrice, position_act, new_position)
    turtle.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche
    return None
    
def deplacer_droite():
    """
    Fonction permettant de se déplacer vers la droite (appel de la fonction deplacer).
    """
    global matrice, position_act
    turtle.onkeypress(None, "Right")  
    new_position = tuple(map(lambda l, k: l + k, position_act, (0, 1)))
    deplacer(matrice, position_act, new_position)
    turtle.onkeypress(deplacer_droite, "Right")   
    return None

def deplacer_haut():
    """
    Fonction permettant de se déplacer vers le haut (appel de la fonction deplacer)
    """
    global matrice, position_act
    turtle.onkeypress(None, "Up")   
    new_position = tuple(map(lambda l, k: l + k, position_act, (-1, 0)))
    deplacer(matrice, position_act, new_position)
    turtle.onkeypress(deplacer_haut, "Up")   
    return None

def deplacer_bas():
    """
    Fonction permettant de se déplacer vers le bas (appel de la fonction deplacer)
    """
    global matrice, position_act
    turtle.onkeypress(None, "Down")   
    new_position = tuple(map(lambda l, k: l + k, position_act, (1, 0)))
    deplacer(matrice, position_act, new_position)
    turtle.onkeypress(deplacer_bas, "Down")  
    return None

def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    Fonction créant un dictionnaire contenant les objets présents associé à leur emplacement (clé).
    Entrée : Fichier txt contenant le liste des objets et de leur emplacement
    """
    dico_objets = {}
    with open(fichier_des_objets, encoding="utf-8") as fichier :
        for ligne in fichier :
            a , b = eval(ligne)
            dico_objets[a] = b
    return dico_objets
    
def deplacement(matrice, position, mouvement) :
    """
    Fonction effectuant les déplacements du personnage.
    Entrée : Matrice(list) du plan, couple(tuple) position actuelle, couple(tuple) future position
    """
    global position_act
    position_act = mouvement
    position = coordonnees(position, largeur_case)
    mouvement = coordonnees(mouvement, largeur_case)
    nvl_pos = tuple(map(lambda l, k: l + k, mouvement, (largeur_case/2, -largeur_case/2)))
    tracer_case(position, COULEUR_VUE, largeur_case)
    turtle.up()
    turtle.color(COULEUR_PERSONNAGE)
    turtle.goto(nvl_pos)
    turtle.down()
    turtle.dot(taille_pers)
    matrice[position_act[0]][position_act[1]] = '0'    

def deplacer(matrice, position, mouvement) :
    """
    Fonction permettant de dessiner les déplacements du personnage (en faisant appel à la fonction deplacement).
    Définit ce qu'il faut faire en fonction de la case sur laquelle le joueur veut se déplacer.
    Entrée : Matrice(list) du plan, couple(tuple) position actuelle, couple(tuple) future position
    """
    global inventaire
    turtle.up()
    #vérifie que la déplacement ne se fais pas hors plan, ni sur un mur ou porte
    if mouvement[0]<len(matrice) and mouvement[1]<len(matrice[1]) :
        if matrice[mouvement[0]][mouvement[1]] == '0' :
            deplacement(matrice, position, mouvement)
        elif  matrice[mouvement[0]][mouvement[1]] == '4' :
            deplacement(matrice, position, mouvement)
            ecriture_annonce(['Vous avez trouvé :  ', dico_objets[position_act]])
            inventaire.add(dico_objets[position_act])
            ecriture_inventaire(dico_objets[position_act])
        elif matrice[mouvement[0]][mouvement[1]] == '3' :
            ecriture_annonce(["Cette porte est fermée."])
            reponse = poser_question(mouvement)
            if reponse == True :
                deplacement(matrice, position, mouvement)
                ecriture_annonce(["Bonne réponse : Porte ouverte."])
            else :
                ecriture_annonce(["Mauvaise réponse."])
        elif matrice[mouvement[0]][mouvement[1]] == '2' :
            deplacement(matrice, position, mouvement)
            ecriture_annonce(["Félicitation, vous avez atteint l'objectif !!"])
    return None

def poser_question(mouvement) :
    """
    Fonction utilisé lors de la rencontre d'une porte. Pose une question au joueur.
    Entrée : Couple(tuple) contenant les coordonnées de la case porte (afin de poser la question associée
    à cette case dans le dictionnaire). 
    Sortie : Retourne True si le joueur à répondu juste, sinon retourne False
    """
    res = False
    reponse_donne = turtle.textinput('Question', dico_questions[mouvement][0])
    turtle.listen() 
    if reponse_donne == dico_questions[mouvement][1] :
        res = True
    return res


#utilitaires
matrice = lire_matrice(fichier_plan) 
largeur_case = calculer_pas(matrice) 
taille_pers = largeur_case*0.9 
dico_objets = creer_dictionnaire_des_objets(fichier_objets) 
dico_questions = creer_dictionnaire_des_objets(fichier_questions) 

#dessin du plan
ecriture_inventaire('Inventaire :') 
afficher_plan(matrice) 
ecriture_annonce(['Vous devez atteindre la case jaune.']) 

#placement du point de départ
position_act = POSITION_DEPART
turtle.up()
turtle.color(COULEUR_PERSONNAGE)
#turtle se place à la position de départ (position_actuelle + la largeur de la case/2 afin que le rond rouge se place en milieu de case) 
#la ligne suivante permet d'additionner 2 tuples
turtle.goto(tuple(map(lambda l, k: l + k, coordonnees(position_act, largeur_case), (largeur_case/2, -largeur_case/2))))
turtle.down()
turtle.dot(taille_pers)

#déplacements
turtle.listen()    # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()    # Place le programme en position d’attente d’une action du joueur












