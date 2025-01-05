"""
Jeu d'Escape Game
Auteurs: Olivia Oumbessilek Babagna et Ayanleh Ismail
Date:17 novembre 2022
Jeu d'Escape Game avec un personnage qui doit trouver la sortie tout en
collectant des objets et traverser des portes
Entree: Plan du chateau et fichiers texte  pour les objets et les portes
Resultat: Jeu interactif avec l'utilisateur
"""
import turtle  # pour tracer la partie graphique

# Definition(initialisation) de constantes globales
pas = 15
position = (0, 1)
positiondot = (-218, 160)
saut = 0
d = {0: 'white', 1: 'grey', 2: 'yellow', 3: 'orange', 4: 'green'}

#Definition des fonctions

def creer_dictionnaire_des_objets(fichier_des_objets):
    '''
    Generation de dictionnaires a partir des fichiers textes
    objets et portes
   Entree:Fichier .txt
   Sortie: dictionnaires(cle:tuple=une position dans le plan,
           valeur=objet/tuple(question,reponse)
    '''
    g = open(fichier_des_objets, encoding='utf-8')
    dico = {}
    for i in g:  # on traite sur chaque du fichier
        a, b = eval(i)
        dico[a] = b  # associe le tuple(position) avec l'objet/ la question/reponse
    return dico  # renvoie le dico complet avec toutes les lignes du fichier traites


def tracer_cadre(long, lag):
    '''
    Trace un rectangle avec longeur/largeur donnee avec le module turtle
    Entree:longeur,largeur(int)
    Sortie:/
    '''
    for i in range(2):
        turtle.forward(long)
        turtle.right(90)
        turtle.forward(lag)
        turtle.right(90)


def tracer_annonces():
    '''
    Trace le cadre d'annonces
    '''
    turtle.tracer(0, 0)
    turtle.penup()
    turtle.hideturtle()
    turtle.goto(-240, 240)
    turtle.pendown()
    tracer_cadre(480, 60)
    turtle.penup()


def tracer_inventaire():
    '''
    Trace le cadre invenntaire
    '''
    turtle.tracer(0, 0)
    turtle.penup()
    turtle.hideturtle()
    turtle.goto(50, 180)
    turtle.pendown()
    tracer_cadre(190, 420)
    turtle.penup()
    turtle.goto(120, 150)
    turtle.write("Inventaire:", align='center')
    turtle.penup()


def lire_matrice(fichier):
    '''
    Generation du plan sous forme de liste a partir d'un fichier
    txt.
    Entree: fichier .txt du plan du chateau
    Sortie: Matrice avec le plan(liste de liste)
    '''
    f = open(fichier)
    lis = []  # initialise la liste pour ajouter les elements des lignes
    lis2 = []  # initialise la liste pour les lignes
    for i in f:  # traitement ligne par ligne
        for j in i:  # traitement element par element par ligne
            if j != ' ' and j != '\n':  # discrimine les elements non numeriques
                a = int(j)
                lis.append(a)  # forme une liste avec les elements
        lis2.append(lis)  #forme une liste avec les liste d'elememts
        lis = []  #reinitialise la liste d'elem pour la prochaine liste
    return lis2


def calculer_pas(matrice):
    """
    Calcule la dimension en pixels turtle des cases du plan
    Entree: la matrice avec le nombre de ligne/colone(liste)
    Sortie: dimension d'une case(int)
    """
    dimension = min(290 // len(matrice[0]), 440 // len(matrice))
    return dimension


def coordonnees(case, pas):
    """
    Calcule les coordonnees turtle d'une case a partir de la dimension
    Entree: case(tuple(ligne,colonne))et pas(int)
    Sortie:coordonne turtle (tuplex(x,y))
    """

    coor0 = -240 + (26 - case[0]) * pas
    coor1 = -240 + case[1] * pas
    return (coor1, coor0)



def tracer_carre(pas):
    """
    Trace un carre
    Entree:dimension turtle(int)
    Sortie:/
    """
    turtle.speed(0)
    turtle.hideturtle()
    turtle.down()
    for i in range(4):
        turtle.forward(pas)
        turtle.left(90)
    turtle.forward(pas)


def tracer_case(case, couleur, pas):
    """
    Trace une case a la bonne place,dans la bonne couleur
    Entree: case=tuple(ligne,colone),couleur(str),pas(int)
    Sortie:/
    """
    turtle.tracer(0, 0)
    turtle.penup()
    turtle.goto(coordonnees(case, pas))
    turtle.color(d[mmatrice[case[0]][case[1]]])
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()
    turtle.update()


def afficher_plan(matrice):
    """
    Affiche le plan complet du chateau
    Entree: matrice-plan du chateau(liste)
    Sortie:/
    """
    for j in range(len(matrice)):  #traitement pour chaque ligne
        for i in range(len(matrice[0])):  #traitement pour chaque element
            tracer_case((j, i), d[matrice[j][i]], calculer_pas(matrice))


def effacer_case(couleur):
    """
    Efface la case souhaitee
    Entree:couleur(str)
    """
    turtle.color(couleur)
    turtle.begin_fill()
    tracer_carre(15)
    turtle.end_fill()
    turtle.penup()


def tracer_personnage(positiondot, position):
    """
    Trace le personnage a la bonne position
    Entree: position du personnage(en coord turtle)(int),
    position(dans la matrice)(int)
    Sortie:/
    """
    turtle.penup()
    turtle.goto(coordonnees(position, 15))
    effacer_case('white')
    turtle.penup()
    turtle.goto(positiondot)
    turtle.pendown()
    turtle.dot(12, 'red')
    turtle.penup()


def new_inventaire(dico, indice, a):
    '''
    Remplis l'inventaire avec l'objet trouve
    Entree: dicotionnaire des objets(dictionnaire),
            position de l'objet dans la matrice(tuple)
            numero de l'objet(int)
    Sortie:/
    '''
    turtle.penup()
    turtle.color('black')
    turtle.goto(70, 130 - (a * 20))
    turtle.pendown()
    turtle.write(dico[(indice[0], indice[1])], align='left')


def annonces_portes(a):
    """
    Trace l'annonce pour les portes
    Entree:numero de l'annonce(int)
    Sortie:/
    """
    turtle.penup()
    turtle.color('black')
    turtle.goto(-230, 200)
    turtle.pendown()
    if a == 1:
        turtle.write("Cette porte est fermée")
    if a == 2:
        turtle.write("La porte s'ouvre")
    if a == 3:
        turtle.write("Mauvaise reponse")
    if a == 4:
        turtle.write("Victoire !")


def new_annonces(dico, indice):
    """
    Affiche une la bonne annonce dans le cadre des annonces
    Entree: dictionnaire objets(dico),position dans la matrice(tuple)
    Sortie:/
    """
    turtle.penup()
    turtle.color('black')
    turtle.goto(-230, 200)
    turtle.pendown()
    turtle.write("Vous avez trouvé :" + ' ' + dico[(indice[0], indice[1])])


def effacer_annonces():
    """
    Efface la precedente annonce
    """
    turtle.penup()
    turtle.color('white')
    turtle.begin_fill()
    turtle.goto(-235, 220)
    tracer_cadre(475, 30)
    turtle.end_fill()
    turtle.penup()


def case_precedente(position):
    """
     Efface la case precedente
     Entree: position dans la matrice(position)
     Sortie:/
    """
    turtle.penup()
    turtle.goto(coordonnees(position, 15))
    effacer_case('wheat')
    turtle.penup()


def deplacer(matrice, position, mouvement, saut):
    '''
    Gestion des deplacements du personnage sur la partie graphique affichee
    Entree: matrice du plan(liste),position actuelle(tuple),
    mouvement souhaite(tuple),nombre d'objets collectes(int)
    Sortie: type de case(vide,porte,objet,objectif)(str)
    '''
    pos2 = (position[0] + mouvement[0], position[1] + mouvement[1])  # calcule prochaine position voulue
    if pos2[0] >= 0 and pos2[0] <= 26 and d[mmatrice[pos2[0]][pos2[1]]] != 'grey': #discrimine les positions du mur ou hors plan
        if d[mmatrice[pos2[0]][pos2[1]]] == 'white': # gestion pour les cases vides
            case_precedente(position)  #efface la case precedente
            resultat = 'Vide' #retiens le type de la case
        if d[mmatrice[pos2[0]][pos2[1]]] == 'green': #gestion pour les objets
            effacer_annonces()
            case_precedente(position)
            new_annonces(dicoobjet, pos2)  #fais une annonce
            new_inventaire(dicoobjet, pos2, saut) #remplis l'inventaire
            resultat = 'objet'  #retiens le type de la case
        if d[mmatrice[pos2[0]][pos2[1]]] == 'orange':  #gestion des portes
            effacer_annonces()
            annonces_portes(1)
            reponse = turtle.textinput('Question', dicoportes[(pos2[0], pos2[1])][0]) #pose la question correspondante a la position
            turtle.listen()
            if reponse == dicoportes[(pos2[0], pos2[1])][1]:  #gestion en cas de bonne reponse
                mmatrice[pos2[0]][pos2[1]] = 0
                case_precedente(position)
                effacer_annonces()
                annonces_portes(2)
                resultat = "porte"  #retiens le type de case
            else:  #gestion en cas de mauvaise reponse
                effacer_annonces()
                annonces_portes(3)
                resultat = '' #retiens un str vide pour une fausse reponse
        if d[mmatrice[pos2[0]][pos2[1]]] == 'yellow':  #gestion pour la sortie du chateau
            effacer_annonces()
            annonces_portes(4)
            case_precedente(position)
            resultat = 'objectif'  #retiens le type de case
        return resultat #renvoie le type de case


def deplacer_gauche():
    """
    Gestion des mouvements sur la gauche
    Entree:/
    Sortie:/
    """
    global mmatrice, position, positiondot, saut
    turtle.onkeypress(None, "Left")
    mouvement = (0, -1)  # mouvement vers la gauche
    situation = deplacer(mmatrice, position, mouvement, saut)  # appelle le type de case ou veut aller le personnage
    if situation == "Vide" or situation == 'objet' or situation == 'porte' or situation == 'objectif':
        position = (position[0] + mouvement[0], position[1] + mouvement[1]) # la position dans le plan-matrice est changee vers la gauche
        positiondot = (positiondot[0] - 15, positiondot[1])  # changement de position du personnage selon le souhait du joueur
        mmatrice[position[0]][position[1]] = 0  # changement du type de case pour les objets et les portes
        tracer_personnage(positiondot, position)  # tracer le personnage a la place souhaitee
        if situation == 'objet':
            saut += 1 # gestion du numero de l'objet
    turtle.onkeypress(deplacer_gauche, "Left")


def deplacer_droite():
    """
      Gestion des mouvements sur la droite
      Entree:/
      Sortie:/
      """
    global mmatrice, position, positiondot, saut
    turtle.onkeypress(None, "Right")
    mouvement = (0, 1)  # mouvement vers la droite
    situation = deplacer(mmatrice, position, mouvement, saut)  # appelle le type de case ou veut aller le personnage
    if situation == "Vide" or situation == 'objet' or situation == 'porte' or situation == 'objectif':
        position = (position[0] + mouvement[0], position[1] + mouvement[1])  # la position dans le plan-matrice est changee vers la droite
        positiondot = (positiondot[0] + 15, positiondot[1])   # changement de position du personnage selon le souhait du joueur
        mmatrice[position[0]][position[1]] = 0  # changement du type de case pour les objets et les portes
        tracer_personnage(positiondot, position)  # tracer le personnage a la place souhaitee
        if situation == 'objet':
            saut += 1  # gestion du numero de l'objet
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_bas():
    """
      Gestion des mouvements vers le bas
      Entree:/
      Sortie:/
      """
    global mmatrice, position, positiondot, saut
    turtle.onkeypress(None, "Down")
    mouvement = (1, 0)  # mouvement vers le bas
    situation = deplacer(mmatrice, position, mouvement, saut)  # appelle le type de case ou veut aller le personnage
    if situation == "Vide" or situation == 'objet' or situation == 'porte' or situation == 'objectif':
        position = (position[0] + mouvement[0], position[1] + mouvement[1])   # la position dans le plan-matrice est changee vers le bas
        positiondot = (positiondot[0], positiondot[1] - 15)  # changement de position du personnage selon le souhait du joueur
        tracer_personnage(positiondot, position)  # tracer le personnage a la place souhaitee
        mmatrice[position[0]][position[1]] = 0  # changement du type de case pour les objets et les portes
        if situation == 'objet':
            saut += 1 # gestion du numero de l'objet
    turtle.onkeypress(deplacer_bas, "Down")


def deplacer_haut():
    """
      Gestion des mouvements vers le haut
      Entree:/
      Sortie:/
      """
    global mmatrice, position, positiondot, saut
    turtle.onkeypress(None, "Up")
    mouvement = (-1, 0)  # mouvement vers le haut
    situation = deplacer(mmatrice, position, mouvement, saut)  # appelle le type de case ou veut aller le personnage
    if situation == "Vide" or situation == 'objet' or situation == 'porte' or situation == 'objectif':
        position = (position[0] + mouvement[0], position[1] + mouvement[1])  # la position dans le plan-matrice est changee vers le haut
        positiondot = (positiondot[0], positiondot[1] + 15)   # changement de position du personnage selon le souhait du joueur
        tracer_personnage(positiondot, position)  # tracer le personnage a la place souhaitee
        mmatrice[position[0]][position[1]] = 0  # changement du type de case pour les objets et les portes
        if situation == 'objet':
            saut += 1  # gestion du numero de l'objet

    turtle.onkeypress(deplacer_haut, "Up")

# Code principal


mmatrice = lire_matrice('plan_chateau.txt')
dicoobjet = creer_dictionnaire_des_objets('dico_objets.txt')
dicoportes = creer_dictionnaire_des_objets('dico_portes.txt')
afficher_plan(lire_matrice('plan_chateau.txt'))
tracer_annonces()
tracer_inventaire()
tracer_personnage(positiondot, position)
turtle.listen()
turtle.onkeypress(deplacer_gauche, "Left")
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()
