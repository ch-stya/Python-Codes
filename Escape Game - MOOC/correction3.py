""" Jeu d'évasion : Quête dans le château au sommet du Python des Neiges

Auteurs : De Sessa Alessandro et Papadopoulos Victoria
Date : 16 novembre 2022
But du jeu : faire sortir le personnage (représenté par un point rouge) du château en le déplaçant dans le labyrinthe,
en trouvant des indices et en ouvrant des portes en répondant à diverses questions.
"""
import turtle

global POINT_AFFICHAGE_INVENTAIRE
global matrice
global position_globale
global pas
global effacer

plan_chateau = "plan_chateau.txt"       # note pour les correcteurs : veuillez remplacer ces fichiers par les fichiers correspondants dans votre ordinateur ( ATTENTION : vous devrez peut-être mettre un "\\" au lieu qu'un simple "\" )
fichier_des_objets = "dico_objets.txt"
fichier_des_portes = "dico_portes.txt"

ZONE_PLAN_MINI = (-240, -240)  # Coin inférieur gauche de la zone d'affichage du plan
ZONE_PLAN_MAXI = (50, 200)  # Coin supérieur droit de la zone d'affichage du plan
POINT_AFFICHAGE_ANNONCES = (-240, 240)  # Point d'origine de l'affichage des annonces
POINT_AFFICHAGE_INVENTAIRE = (70, 210)  # Point d'origine de l'affichage de l'inventaire

COULEUR_CASES = 'white'
COULEUR_COULOIR = 'white'
COULEUR_MUR = 'grey'
COULEUR_OBJECTIF = 'yellow'
COULEUR_PORTE = 'orange'
COULEUR_OBJET = 'green'
COULEUR_VUE = 'wheat'
COULEUR_EXTERIEUR = 'white'

POSITION_DEPART = (0, 1)
COULEUR_PERSONNAGE = 'red'
RATIO_PERSONNAGE = 0.9

'''
Cette fonction transforme un fichier donné en dictionnaire
'''
def creer_dictionnaire_des_objets(fichier_des_objets):
    with open(fichier_des_objets, "r", encoding = "utf-8") as objets:    # ceci permet de mettre le nom du fichier comme argument de la fonction
        dico_objets = {}
        for i in objets:
            a,b = eval(i)
            dico_objets[a] = b
    return dico_objets

'''
Cette fonction transforme un fichier donné en une matrice
'''
def lecture_matrice(fichier):
    with open(fichier,"r", encoding = "utf-8") as file:        # ceci permet de mettre le nom du fichier comme argument de la fonction
        matrice=[]
        new_matrice=[]
        mini_matrice=[]
        for i in file:                   # transforme le doc en une seule liste de chaines de caractères
            matrice.append(i.strip())
        for b in range(len(matrice)):
            for a in range(0,len(matrice[b]),2):
                mini_matrice.append(int(matrice[b][a]))   # transforme le premier élement de la liste de chaines de caractères en une sous-liste d'int
            new_matrice.append(mini_matrice)              # ajoute cette sous-liste à la liste finale
            mini_matrice=[]
    return new_matrice

'''
Cette fonction calcule le pas ( le côté d'une case ) à partir du plan du chateau ( et de la zone d'affichage du plan )
'''
def calculer_pas(plan_chateau):            # calcule le côté d'un carré sur base du plan donné
    h = abs(ZONE_PLAN_MAXI[1]) + abs(ZONE_PLAN_MINI[1])
    l = abs(ZONE_PLAN_MAXI[0]) + abs(ZONE_PLAN_MINI[0])
    largeur = lecture_matrice(plan_chateau)
    cote_l = l//len(largeur[0])    # divise la longueur de l'espace d'affichage du chateau par la longueur ( en nombre de cases ) du chateau
    cote_h = h//len(largeur)       # divise la hauteur de l'espace d'affichage du chateau par la hauteur ( en nombre de cases ) du chateau
    return min(cote_l,cote_h)  # renvoie la taille d'un côté du carré

'''
Cette fonction calcule les coordonnées du coin inférieur gauche d’une case définie par sa ligne, sa colonne et par le pas
( case est un tuple contenant la ligne et la colonne de la case )
'''
def coordonnees(case, pas):
    ligne = case[0]
    colonne = case[1]
    x = ZONE_PLAN_MINI[0] + pas*colonne
    y = ZONE_PLAN_MAXI[1]-pas*ligne
    return x,y # renvoie le coin inférieur gauche de la case

'''
Cette fonction permet de tracer un carré dont la dimension est donnée en argument
'''
def tracer_carre(dimension):
    for i in range (4):
        turtle.forward(dimension)
        turtle.left(90)

'''
Cette fonction permet de tracer une case ( dont la ligne et colonne sont donnés en argument car "case"est un tuple ) 
en une couleur donnée en argument et de pas donné en argument
'''
def tracer_case(case, couleur, pas):
    turtle.hideturtle()
    turtle.up()
    turtle.goto(coordonnees(case,pas))
    turtle.down()
    turtle.color(couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()
    turtle.color(COULEUR_EXTERIEUR)
    tracer_carre(pas)

'''
Cette fonction permets d'afficher le plan du chateau, 
il fait cela en prenant la matrice représentant le plan 
du chateau en argument
'''
def afficher_plan(matrice): # permet d'afficher les différentes cases qui composent le plan du chateau
    for i in range(len(matrice)):           # ces 2 lignes de codes parcourent tous les éléments de la matrice représentant le plan du chateau
        for k in range(len(matrice[i])):
            if matrice[i][k] == 0: # affiche les cases 'vides' du château
                tracer_case((i,k),COULEUR_CASES,pas)
            elif matrice[i][k] == 1: # affiche les cases du mur composant le château
                tracer_case((i,k),COULEUR_MUR,pas)
            elif matrice[i][k] ==2: # affiche la dernière case à atteindre pour sortir du château
                tracer_case((i,k),COULEUR_OBJECTIF,pas)
            elif matrice[i][k] ==3: # affiche les cases des portes du château
                tracer_case((i,k),COULEUR_PORTE,pas)
            elif matrice[i][k] ==4: # affiche les cases des coffres du château
                tracer_case((i,k),COULEUR_OBJET,pas)

'''
Cette fonction renvoie la position du personnage en coordonnées 
en prenant la case ( tuple composé de la ligne et colonne de la
case dans la matrice représentant le plan du chateau ) et le pas 
en argument
'''
def position_personnage(case,pas):
    x,y = coordonnees(case,pas)
    return x+pas/2, y+pas/2 # renvoie les coordonnées du centre de la case qu'on souhaite

'''
Cette fonction permet au joueur de récolter les objets 
( en affichant une annonce à l'écran et en ajoutant l'objet
à l'inventaire )

Cette fonction prends la position du personnage et la nouvelle position du personnage en argument
'''
def ramasser_objets(position,nouvelle_position):
    global POINT_AFFICHAGE_INVENTAIRE
    annonce.clear() # efface l'annonce précédente
    tracer_case((nouvelle_position[0], nouvelle_position[1]), COULEUR_VUE, pas) #trace une case sur la nouvelle position du personnage ( sur la case objet ) avec la couleur d'une case vue
    tracer_case((position[0], position[1]), COULEUR_VUE, pas) # trace une case sur la position du personnage ( et donc couvre le personnage )
    turtle.up()
    turtle.goto(position_personnage(nouvelle_position, pas))
    turtle.down()
    turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)  #dessine le personnage sur la case objet
    annonce.up() # commence le processus d'affichage du message après avoir débloquer l'indice
    annonce.color('black')
    annonce.goto(POINT_AFFICHAGE_ANNONCES)
    annonce.down()
    annonce.write("Vous avez trouvé : " + dico_objets[nouvelle_position]) # affiche le message contenant l'indice
    turtle.up() # place l'objet dans l'inventaire en l'y inscrivant
    turtle.color('black')
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    turtle.down()
    turtle.write("-" + dico_objets[nouvelle_position])
    a, b = POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] # change la valeur du point affichage de l'inventaire pour faire en sorte qu'au prochain appel de la fonction l'indice sera écrit en dessous du précédent
    POINT_AFFICHAGE_INVENTAIRE = (a, b - 15)
    matrice[nouvelle_position[0]][nouvelle_position[1]] = 0 # transforme la case objet en case vide dans la matrice représentant le plan du chateau

'''
Cette fonction permets au joueur d'intéragir avec les portes 
( cela implique afficher des annonces, poser des questions pour 
ouvrir la porte et vérifier que la réponse donnée est correcte )

La fonction prends la matrice représentant le plan du chateau, 
la case ( où se trouve le joueur ) et le mouvement en argument
'''
def poser_question(matrice, case, mouvement):
    global position_globale
    global effacer
    annonce.clear()
    nouvelle_position = case[0] + mouvement[0], case[1] + mouvement[1]  # calcule la nouvelle case sur laquelle le personnage doit aller
    annonce.up()  # affiche une annonce, en l'occurence que la porte est fermée
    annonce.color('black')
    annonce.goto(POINT_AFFICHAGE_ANNONCES)
    annonce.down()
    annonce.write("Cette porte est fermée.")
    réponse = turtle.textinput("Question: ", dico_portes[nouvelle_position][0]) # pose une question qui va permettre d'ouvrir une porte
    if réponse == dico_portes[nouvelle_position][1]: # permet d'ouvrir la porte si la réponse est correcte
        tracer_case((nouvelle_position[0], nouvelle_position[1]), COULEUR_VUE, pas) #trace une case sur la nouvelle position du personnage ( sur la case objet ) avec la couleur d'une case vue
        tracer_case((case[0], case[1]), COULEUR_VUE, pas)     # trace une case sur la position du personnage ( et donc couvre le personnage )
        matrice[nouvelle_position[0]][nouvelle_position[1]] = 0 # transforme la case porte en case vide dans la matrice représentant le plan du chateau
        global position_globale
        position_globale = nouvelle_position # mets à jour la position du personnage
        annonce.clear()
        annonce.write("La porte est ouverte !") # affiche une nouvelle annonce ( que la porte est ouverte )
        effacer = 1 # change la valeur de la variable effacer pour faire en sorte que le message "porte ouverte" s'efface au prochain mouvement du personnage ( voire fonction déplacer )
    turtle.listen() # turtle.textinput() arrête turtle.listen() : il faut donc re-écrire la commande

'''
Cette fonction affiche le message de fin du jeu
'''
def victoire():
    turtle.clear()
    turtle.goto(0, 0)
    turtle.color('black')
    turtle.write("GAGNÉ !", False, "center", ("Arial", 50, "bold"))

'''
Cette fonction permet au personnage de se déplacer dans le plan,
elle prends la matrice représentant le plan du chateau, la position 
du personnage et le mouvement du personnage en argument
'''
def deplacer(matrice,position,mouvement): # défini le déplacement du personnage
    turtle.onkeypress(None, "Right")  # ces 4 lignes ne permettent plus au joueur d'appeler les 4 fonctions de déplacement ( ce code sert à éviter des bugs qui s'avèrent lorsque le joueur appuie trop rapidement sur les touches de déplacement )
    turtle.onkeypress(None, "Left")
    turtle.onkeypress(None, "Up")
    turtle.onkeypress(None, "Down")
    global effacer
    if effacer == 1:  # efface les annonces affichées auparavant
        annonce.clear()
        effacer = 0
    nouvelle_position = position[0] + mouvement[0], position[1] + mouvement[1] # calcule la nouvelle position du personnage
    if matrice[nouvelle_position[0]][nouvelle_position[1]] != 1: # ce code empêche le joueur de traverser des murs
        if matrice[nouvelle_position[0]][nouvelle_position[1]] == 4: # la fonction ramasser_objets est appelée si le personnage bouge sur une case "objet"
            ramasser_objets(position, nouvelle_position)
        elif matrice[nouvelle_position[0]][nouvelle_position[1]] == 3: # la fonction poser_question est appelée si le personnage bouge sur une case "porte"
            poser_question(matrice, position, mouvement)
            effacer = 1 # permet d'effacer l'annonce au prochain mouvement du personnage
        elif matrice[nouvelle_position[0]][nouvelle_position[1]] == 2:
            tracer_case((position[0], position[1]), COULEUR_VUE, pas)  # affiche l'annonce de fin après avoir terminé le jeu
            victoire()
        elif matrice[position[0]][position[1]] == 0: # colorie les cases vues par le personnage
            tracer_case((position[0], position[1]), COULEUR_VUE, pas)
        elif matrice[position[0]][position[1]] == 4: # colorie les cases objets vues par le personnage
            tracer_case((position[0], position[1]), COULEUR_VUE, pas)
        if matrice[nouvelle_position[0]][nouvelle_position[1]] != 3 and matrice[nouvelle_position[0]][nouvelle_position[1]] != 2: # permet au personnage de ne pas traverser les portes et de ne pas s'afficher quand le jeu est terminé
            turtle.up()
            turtle.goto(position_personnage(nouvelle_position, pas))
            turtle.down()
            turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
            global position_globale
            position_globale = nouvelle_position # mets à jour la position du personnage
    if matrice[nouvelle_position[0]][nouvelle_position[1]] != 2: # empêche le joueur de bouger le personnage quand le jeu est terminé
        turtle.onkeypress(deplacer_droite, "Right") #ces 4 lignes permettent au joueur d'appeler les 4 fonctions déplacer à nouveau
        turtle.onkeypress(deplacer_gauche, "Left")
        turtle.onkeypress(deplacer_haut, "Up")
        turtle.onkeypress(deplacer_bas, "Down")

'''
Cette fonction permet de déplacer le personnage vers la droite
'''
def deplacer_droite(): # permet de déplacer le personnage vers la droite
    global matrice
    global position_globale
    deplacer(matrice, position_globale, (0, 1)) # (0,1) permet le déplacement d'une case vers la droite

'''
Cette fonction permet de déplacer le personnage vers la gauche
'''
def deplacer_gauche(): # permet de déplacer le personnage vers la gauche
    global matrice
    global position_globale
    deplacer(matrice,position_globale,(0,-1)) # (0,-1) permet le déplacement d'une case vers la gauche

'''
Cette fonction permet de déplacer le personnage vers le haut
'''
def deplacer_haut(): # permet de déplacer le personnage vers le haut
    global matrice
    global position_globale
    deplacer(matrice, position_globale, (-1, 0)) # (-1, 0) permet le déplacement d'une case vers le haut

'''
Cette fonction permet de déplacer le personnage vers le bas
'''
def deplacer_bas(): # permet de déplacer le personnage vers le bas
    global matrice
    global position_globale
    deplacer(matrice, position_globale, (1, 0)) # (1, 0) permet le déplacement d'une case vers le bas

turtle.tracer(False) # élimine les animations de turtle
turtle.hideturtle()
annonce = turtle.Turtle() #crée une turtle dédiée à l'affichage d'annonces
annonce.hideturtle()

dico_objets = creer_dictionnaire_des_objets(fichier_des_objets)  # transforme le fichier des objets en dictionnaire
dico_portes = creer_dictionnaire_des_objets(fichier_des_portes)  # transforme le fichier des portes en dictionnaire
matrice = lecture_matrice(plan_chateau)  # transforme le fichier du plan du chateau en matrice
pas = calculer_pas(plan_chateau)  # donne à la variable pas le pas du plan du chateau
effacer = 0 # donne une valeur initiale à la variable globale effacer
position_globale = POSITION_DEPART # assigne à la variable position globale la valeur de la variable POSITION_DEPART


afficher_plan(matrice) # affiche le plan du chateau
turtle.up()
turtle.goto(POINT_AFFICHAGE_INVENTAIRE) # affiche l'inventaire
turtle.color('black')
turtle.down()
turtle.write("Inventaire :", False, 'left', ('Arial', '10', 'normal'))
turtle.up()
a, b = POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1]  # change la valeur du point affichage de l'inventaire pour faire en sorte que le premier indice trouvé sera affiché en dessous de "Inventaire :"
POINT_AFFICHAGE_INVENTAIRE = (a, b - 15)
turtle.goto(position_personnage(position_globale,pas))  # le personnage va au point de départ
turtle.down()
turtle.dot(RATIO_PERSONNAGE*pas, COULEUR_PERSONNAGE)

turtle.listen()  # permet au joueur de se déplacer en appuyant sur les flèches du clavier
turtle.onkeypress(deplacer_gauche, 'Left')
turtle.onkeypress(deplacer_droite, 'Right')
turtle.onkeypress(deplacer_haut, 'Up')
turtle.onkeypress(deplacer_bas, 'Down')
turtle.mainloop()
