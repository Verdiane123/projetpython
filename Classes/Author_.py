class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}

    def add_document(self, document):
        # Ajouter un document écrit par l'auteur
        self.ndoc += 1
        self.production[self.ndoc] = document

    def __str__(self):
        return f"Author: {self.name}, Number of Documents: {self.ndoc}"
