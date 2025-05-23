"""
Exercice : Programmation procédurale
Créer un programme qui permet de gérer les notes d'étudiants dans 
différentes matières et de calculer diverses statistiques. 
Les matières sont : Mathématiques, Physique, et Informatique 
Chaque matière a un coefficient : Mathématiques (4), Physique (3), 
Informatique (3)
QUESTIONS :
Fonctionnalités à implémenter :
1. Saisie des notes d'un étudiant 
2. Calcul de la moyenne pondérée 
3. Calcul du rang et mention 
4. Affichage du bulletin
"""
def main():
    etudiant = input("Veuillez indiquer le nom de l'etudiant : ")
    saisie_note()

def saisie_note():
    liste_matiere = ["Mathématiques", "Physique", "Informatique"]
    notes = {}
    for matiere in liste_matiere :
        try :
            note = int(input(f"Veuillez indiquer la note obtenue en {matiere} : "))
            if (note <= 20 and note >= 0 ) : 
                print(f"La note obtenue en {matiere} est de {note}/20.")
                notes[matiere] = note
            else :
                print("Veuillez saisir une note se trouvant entre 0 et 20.")
        except : 
            print("Veuillez saisir une valeur numérique.")

def calcul_moyenne():
    coef = {("Mathématiques", 4), ("Physique", 3), ("Informatique", 3)}

main()


    
    
