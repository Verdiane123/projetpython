class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

# Méthode add permettant d'avoir de nouvelles productions. 
    def add(self, production):    # Production représente l'ensemble des oeuvres d'un auteur
        self.ndoc += 1
        self.production.append(production)

    def __str__(self):
        return f"Auteur : {self.name}\t# Productions : {self.ndoc}"
    