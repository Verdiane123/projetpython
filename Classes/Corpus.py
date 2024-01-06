import re
from .Author import Author

class Corpus:
    global_corpus_string = None

    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def ajouterDocument(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        print("Global Corpus String après l'ajout:", Corpus.global_corpus_string)

    def build_global_corpus_string(self):
        if Corpus.global_corpus_string is None:
            Corpus.global_corpus_string = " ".join(str(doc) for doc in self.id2doc.values())


    def search(self, keyword):
        matches = []
        for doc in self.id2doc.values():
            doc_matches = re.findall(fr'\b{re.escape(keyword)}\b', doc.texte, flags=re.IGNORECASE)
            matches.extend(doc_matches)

        return matches

    # def search(self, keyword):
    #     self.build_global_corpus_string()
    #     print("Global Corpus String:", Corpus.global_corpus_string)
    #     print("Keyword:", keyword.lower())
        
    #     # Convertissez les deux en minuscules pour assurer la correspondance insensible à la casse
    #     matches = re.findall(fr'\b{re.escape(keyword.lower())}\b', Corpus.global_corpus_string.lower(), flags=re.IGNORECASE)
        
    #     print("Matches:", matches)
    #     return matches




    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc": # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123": #Tri par date
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

# Pour une affichage plus digeste des résultats par titre
    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))




