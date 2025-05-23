"""
Contexte : Vous devez concevoir un système pour gérer des objets représentant des 
véhicules dans un parking. Chaque véhicule a un numéro d’immatriculation, une marque, et 
un type (par exemple voiture, moto, camion).
1. Définissez une hiérarchie de classes en utilisant les concepts d’héritage et de 
polymorphisme pour modéliser ce système (par exemple, une classe parent Véhicule 
et des classes enfants Voiture, Moto, etc.).
2. Implémentez une méthode polymorphique afficher_details() qui affiche les 
informations spécifiques selon le type de véhicule.
3. Ajoutez une classe Parking qui permet d'ajouter et de supprimer des véhicules à partir 
d'une liste. Cette classe devra être générique pour pouvoir gérer tous les types de 
véhicules.
Indications : Fournissez le code Python des classes et méthodes, et expliquez brièvement 
comment l’héritage et le polymorphisme sont utilisés.

"""

class Vehicule:
    def __init__(self, immatriculation, marque):
        self.immatriculation = immatriculation
        self.marque = marque

    def afficher_details(self):
        print(f"L'immatriculation du véhicule est : {self.immatriculation}.")
        print(f"La marque du véhicule est : {self.marque}.")

class Voiture(Vehicule):
    def __init__(self, immatriculation, marque):
        super().__init__(immatriculation, marque)
        self.type = "voiture"

    def afficher_details(self):
        super().afficher_details()
        print(f"Ce véhicule est une {self.type}.")

class Moto(Vehicule):
    def __init__(self, immatriculation, marque):
        super().__init__(immatriculation, marque)
        self.type = "moto"

    def afficher_details(self):
        super().afficher_details()
        print(f"Ce véhicule est une {self.type}.")

class Parking:
    def __init__(self, nb_places, nb_places_prises=0):
        self.nb_places = nb_places
        self.nb_places_prises = nb_places_prises
        self.liste_vehicules = []

    def afficher_places_disponibles(self):
        nb_places_restantes = self.nb_places-self.nb_places_prises
        print(f"Places restantes : {nb_places_restantes}.")
        if nb_places_restantes == self.nb_places-1 :
            print(f"Véhicule garé sur le parking :")
            for vehicule in self.liste_vehicules :
                print(f"- {vehicule.type} {vehicule.marque} ({vehicule.immatriculation})")
        elif nb_places_restantes != self.nb_places :
            print(f"Véhicules garés sur le parking :")
            for vehicule in self.liste_vehicules :
                print(f"- {vehicule.type} {vehicule.marque} ({vehicule.immatriculation})")
        else :
            print("Le parking est vide.")

    def ajouter_vehicule(self, vehicule):
        self.liste_vehicules.append(vehicule)
        self.nb_places_prises += 1
        self.afficher_places_disponibles()

    def supprimer_vehicule(self, vehicule):
        self.liste_vehicules.remove(vehicule)
        self.nb_places_prises -= 1
        self.afficher_places_disponibles()

mercedes_toto = Voiture("OK-226-DB", "Mercedes")
moto_tata = Moto("AB-123-DZ", "Toyota")
mercedes_toto.afficher_details()
moto_tata.afficher_details()
parking_parc = Parking(200)
parking_parc.ajouter_vehicule(moto_tata)
parking_parc.supprimer_vehicule(moto_tata)

