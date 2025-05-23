"""
Exercice : Paradigme Objet (Python) – Gestion d'un Réseau Social 
Créez une classe Utilisateur qui a pour attributs nom, email, et amis, où 
amis est une liste d'autres instances de la classe Utilisateur. 
Ajoutez une méthode ajouter_ami pour ajouter un ami, et une méthode 
afficher_reseau qui affiche tous les amis d'un utilisateur ainsi que les amis 
de ses amis jusqu'à deux niveaux.
Ensuite, créez une sous-classe UtilisateurPremium qui permet d'ajouter 
une méthode afficher_statistiques pour afficher le nombre d'amis d'un 
utilisateur premium.
QUESTIONS :
1. Implémentez les classes Utilisateur et UtilisateurPremium avec les 
méthodes demandées.
2. Ajoutez une méthode supprimer_ami pour permettre à un utilisateur 
de supprimer un ami de sa liste.
"""

class Utilisateur:
    # Constructeur
    def __init__(self, nom, email):
        self.nom = nom
        self.email = email
        self.amis = []

    def ajouter_ami(self, ami):
        self.amis.append(ami)
        ami.amis.append(self)
        print(f"Ajout de l'ami : {ami.nom}.")

    def afficher_reseau(self, niveau=0):
        if (niveau<=2):
            if len(self.amis)==0 :
                print(f"{self.nom} n'a pas encore ajouté d'amis.")
            else :
                for ami in self.amis :
                    print(f"Liste d'amis de {self.nom} : {ami.nom}")
                    ami.afficher_reseau(niveau+1)

    def supprimer_ami(self, ami):
        self.amis.remove(ami)
        ami.amis.remove(self)
        print(f"Suppression de l'ami : {ami.nom}.")

class UtilisateurPremium(Utilisateur):
    def afficher_statistiques(self):
        print(f"Nombre d'amis de {self.nom} : {len(self.amis)}")

toto = Utilisateur("Toto", "toto@gmail.com")
tata = UtilisateurPremium("Tata", "tata@gmail.com")

toto.ajouter_ami(tata)
toto.afficher_reseau()
tata.afficher_statistiques()
tata.supprimer_ami(toto)
toto.afficher_reseau()
