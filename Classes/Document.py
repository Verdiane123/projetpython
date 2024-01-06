class Document:
    # Initialisation des variables
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    # def infosTextes(self):
    #      print(f"Titre: {self.titre}")
    #      print(f"Auteur: {self.auteur}")
    #      print(f"Date de publication: {self.date}")
    #      print(f"URL: {self.url}")
    #      print(f"Texte: {self.texte}")

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
