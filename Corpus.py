from Author import Author
import pickle
import re
import pandas as pd

class Corpus:
    global_corpus_string = None
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2aut = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.id2aut:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.id2aut[doc.auteur] = self.naut
        self.authors[self.id2aut[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

        # Appeler la méthode build_global_corpus_string après chaque ajout de document
        self.build_global_corpus_string()

    #Construction global du corpus
    def build_global_corpus_string(self):
        if Corpus.global_corpus_string is None:
            Corpus.global_corpus_string = " ".join(str(doc) for doc in self.id2doc.values())

    # =============== Méthodes pour l'affichage du corpus ===============
    #Affichage avec tri par titre/ou par date
    def show(self, n_docs, tri=""):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        return docs
        #print("\n".join(list(map(repr, docs))))

    #Affichage plus digeste
    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

    #Enregitrement du corpus sur le disque avec pickle
    def save(self, file_path):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)
        print(f"Le corpus a été enregistré avec succès dans {file_path}")

    #Chargement du corpus depuis le disque
    def load(cls, file_path):
        with open(file_path, "rb") as file:
            loaded_corpus = pickle.load(file)
        print(f"Le corpus a été chargé avec succès depuis {file_path}")
        return loaded_corpus
     
#----------TD6---------------
    #FONCTION QUI PERMET DE CHERCHER UN MOT dans le corpus
    def search(self, keyword):
        matches = []
        for doc in self.id2doc.values():
            doc_matches = re.findall(fr'\b{re.escape(keyword)}\b', doc.texte, flags=re.IGNORECASE)
            matches.extend(doc_matches)

        return matches
    
    #FONCTION QUI PERMET DE CHERCHER UNE EXPRESSION dans le corpus
    def concorde(self, expression, context_size):
        results = []

        for doc_id, doc in self.id2doc.items():
            matches = re.finditer(fr'\b{re.escape(expression)}\b', doc.texte, flags=re.IGNORECASE)
            
            for match in matches:
                start = max(0, match.start() - context_size)
                end = min(len(doc.texte), match.end() + context_size)
                
                left_context = doc.texte[start:match.start()].strip()
                right_context = doc.texte[match.end():end].strip()
                
                result = {
                    'ID du document': doc_id,
                    'Contexte gauche': left_context,
                    'Motif trouvé': match.group(),
                    'Contexte droit': right_context
                }
                
                results.append(result)
        
        df = pd.DataFrame(results)
        return df
        
    #FONCTION QUI PERMET DE FORMATER UN TEXTE (PAR EXEMPLE: TRANSFORMER LES MAJ EN MINUSCULE ET D'ENLEVER LES PONCTUATIONS)
    def nettoyer_texte(self, texte):
        # Mettre en minuscules
        texte = texte.lower()

        # Remplacer les passages à la ligne par un espace
        texte = texte.replace('\n', ' ')

        # Remplacer les ponctuations par un espace
        texte = re.sub(r'[^\w\s]', ' ', texte)

        # Remplacer les chiffres par un espace
        texte = re.sub(r'\d', ' ', texte)

        # Supprimer les espaces multiples
        texte = re.sub(r'\s+', ' ', texte).strip()

        return texte

#chaine_unique = " ".join(self.id2doc.values)
#print(chaine_unique)
    
    #Méthode stats pour avoir afficher quelques statistiques textuelles sur le corpus
    def stats(self, n):
        occurence = {} #pinitialisation d'un dictionnaire pour stocker les occurences des clés
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte) #Nettoyage du texte du corpus
            dic = texte_nettoye.split(' ') #Séparation des mots du texte
            ensemble = set(dic) #Contruction d'un ensemble pour éliminer les doublons
            vocabulaire = dict.fromkeys(ensemble) #contruction du vocabulaire pour décrire les documents
        
        print(vocabulaire.items())

        #Compter le nombre d'occurence de chaque mot du vocabulaire
        for mot in vocabulaire:
            if mot in occurence:
                occurence[mot] +=1
            else:
                occurence[mot] = 1
                
        #Afficher le nombre de mots différents dans le corpus
        print("Le nombre de mots différents dans le corpus : ",len(vocabulaire)) 
        
        #Afficher les n mots les plus fréquents
        occurence_trie = sorted(occurence, key=occurence.get, reverse=True) #tri du dictionnaire par valeur descendante de chaque clé
        print("Les n mots les plus fréquents dans le corpus : ",occurence_trie[:n])
