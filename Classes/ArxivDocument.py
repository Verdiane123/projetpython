# Importing the Document class from the existing code
import ipywidgets as widgets
import Document, Author

# Partie 2

# Définir la classe ArxivDocument en tant que sous-classe de Document
class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", co_auteurs=None):
        # Appeler le constructeur de la classe parente (Document)
        super().__init__(titre, auteur, date, url, texte)
        # Ajouter le nouveau champ spécifique à ArXiv
        self.co_auteurs = co_auteurs if co_auteurs is not None else []

    # Accesseur et mutateur pour le champ co_auteurs
    def get_co_auteurs(self):
        return self.co_auteurs

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    # Remplacer la méthode __str__ pour une représentation personnalisée
    def __str__(self):
        return f"{super().__str__()}, Co-auteurs : {', '.join(self.co_auteurs)}"
    
    def getType(self):
        return "Hello ArXiv"

# Exemple d'utilisation :
# Créer une instance de ArxivDocument
arxiv_doc = ArxivDocument(titre="Exemple d'article ArXiv", auteur="AuteurPrincipal", date="2023/01/01", url="https://arxiv.org/exemple", texte="Résumé de l'article.", co_auteurs=["CoAuteur1", "CoAuteur2"])

# Afficher l'instance de ArxivDocument
print(arxiv_doc)

# Partie 3
class Corpus:
    # ...
    def __init__(self):
        self.nom = ""
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if isinstance(doc, Document):  # Vérifier si doc est une instance de Document ou de ses sous-classes
            if doc.auteur not in self.aut2id:
                self.naut += 1
                self.authors[self.naut] = Author(doc.auteur)
                self.aut2id[doc.auteur] = self.naut
            self.authors[self.aut2id[doc.auteur]].add(doc.texte)

            self.ndoc += 1
            self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        # print("\n".join(list(map(repr, docs))))
        for doc in docs:
            print(f"{doc.getType()}: {repr(doc)}")

# ...

# Exemple d'utilisation du polymorphisme avec la classe Corpus
corpus = Corpus()
corpus.nom = "Mon corpus"