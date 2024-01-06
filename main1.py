# Importation des bibliothèques et des classes
import praw
import urllib.request
import xmltodict
import numpy as np
import pickle
import pandas as pd
import datetime
from Classes.Document import Document
from Classes.Author import Author
from Classes.Corpus import Corpus


# Paramétrage de l'accès à Reddit avec nos identifiants
reddit = praw.Reddit(client_id='n1qq6DaTnsjSXFereBgjtw', client_secret='ee0gpDJWspWfBCw3kcuk30vOyWregA', user_agent='Verdiane')

# Récupération des données (textes, auteurs et années de parution) depuis Reddit sur la base de notre thématique : le FOOTBALL
subr = reddit.subreddit('Football')
textes_Reddit = []   
auteurs_Reddit = []  
annees_Reddit = []   



for post in subr.hot(limit=100):
    texte = post.title
    texte = texte.replace("\n", " ")
    textes_Reddit.append(texte)
    auteurs_Reddit.append(post.author.name)  
    annees_Reddit.append(post.created_utc)  #extraction de l'année de parution avec la clé created_utc

# Récupération des données depuis ArXiv avec les mêmes options que Reddit
textes_Arxiv = []
auteurs_Arxiv = []  
annees_Arxiv = []   
query = "football"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()
data = url_read.decode()
dico = xmltodict.parse(data)
docs = dico['feed']['entry']

for d in docs:
    texte = d['title'] + ". " + d['summary']
    texte = texte.replace("\n", " ")
    textes_Arxiv.append(texte)
    # Extraction des noms des auteurs
    auteurs = [a['name'] if isinstance(a, dict) and 'name' in a else a for a in d.get('author', [])]
    auteurs_Arxiv.append(auteurs)  
    annees_Arxiv.append(int(d['published'][:4]))  #extraction avec la clé 'published' pour Arvix

# Concaténation des textes
corpus = textes_Reddit + textes_Arxiv
print("Longueur du corpus : " + str(len(corpus)))

# Affichage des auteurs et des années de parution des textes
print("Auteurs Reddit : ", auteurs_Reddit)
print("Années Reddit : ", [datetime.datetime.utcfromtimestamp(annee).year for annee in annees_Reddit])
print("Auteurs ArXiv : ", auteurs_Arxiv)
print("Années ArXiv : ", annees_Arxiv)

# Création d'une collection sous forme de dictionnaire pour associer des identifiants aux objets Document
id2doc = {}
id2aut = {}
index_document = 1

# Récupération des données depuis Reddit
for i, (texte, auteur, annee) in enumerate(zip(textes_Reddit, auteurs_Reddit, annees_Reddit), start=index_document):
    # Vérification de l'existence de l'auteur 
    if auteur not in id2aut:
        id2aut[auteur] = Author(name=auteur)

    doc = Document(
        titre=f"Document Reddit {i+1}",
        auteur=auteur,
        date=datetime.datetime.utcfromtimestamp(annee).strftime("%Y-%m-%d"),
        url="",
        texte=texte
    )

    # Mettre à jour des infos de l'auteur
    id2aut[auteur].add(doc)

    # Ajout de l'instance Document au dictionnaire id2doc
    id2doc[index_document] = doc
    index_document += 1

# Récupération des données depuis ArXiv
for i, (texte, auteurs, annee) in enumerate(zip(textes_Arxiv, auteurs_Arxiv, annees_Arxiv), start=index_document):
    # Même scénario de vérification pour Arvix
    if auteur not in id2aut:
        id2aut[auteur] = Author(name=auteur)

    doc = Document(
        titre=f"Document ArXiv {i+1}",
        auteur=", ".join(auteurs),
        date=str(annee),
        url="",
        texte=texte
    )

    # Mise à jour
    id2aut[auteur].add(doc)

    id2doc[index_document] = doc
    index_document += 1

  


# Création d'une instance de Corpus
mon_corpus = Corpus(nom="Corpus 2024")

# Ajout des documents au corpus
for i, doc in id2doc.items():
    mon_corpus.ajouterDocument(doc)

# Affichage des documents triés par titre
print("Affichage des documents par titre:")
mon_corpus.show(n_docs=5, tri="abc")

# Affichage des documents triés par date
print("\nAffichage des documents par date:")
mon_corpus.show(n_docs=5, tri="123")

# Recherche de mots-clés dans le corpus
keyword = "football"
occurence = mon_corpus.search(keyword)
nombre_occurence = len(occurence)
#print(f"\nOccurrences du mot-clé '{keyword}' dans le corpus : {occurence}")
print(f"\nNombre d'occurrences du mot-clé '{keyword}' dans le corpus : {nombre_occurence}")


  # Demander des statistiques d'un auteur 
requete_auteur = input("\nEntrez le nom de l'auteur recherché : ")
if requete_auteur in mon_corpus.aut2id:
    statistique_auteur = mon_corpus.authors[mon_corpus.aut2id[requete_auteur]]
    print(f"Statistiques de {statistique_auteur.name}:")
    print(f"Nombre de documents publiés : {statistique_auteur.ndoc}")
    if statistique_auteur.ndoc > 0:
        taille_moyenne = np.mean([len(texte) for texte in statistique_auteur.production])
        print(f"Taille moyenne des documents : {taille_moyenne:.2f} caractères")
else:
    print(f"Désolé ! L'auteur {requete_auteur} n'est pas connu. 😕")


# Affichage des informations des documents dans la collection
# for i, doc in id2doc.items():
#      print(f"Document {i}:")
#      doc.infosTextes()
#      print()

# Analyse statistique des textes
for doc in corpus:
    # Nombre de phrases
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))

nombre_phrases = [len(doc.split(".")) for doc in corpus]
print("Nombre moyen de phrases : " + str(np.mean(nombre_phrases)))

nombre_mots = [len(doc.split(" ")) for doc in corpus]
print("Nombre moyen de mots : " + str(np.mean(nombre_mots)))

print("Nombre total de mots dans le corpus : " + str(np.sum(nombre_mots)))

#Filtrage des documents de plus de 100 caractères
corpus_plus100 = [doc for doc in corpus if len(doc) > 100]

#Sauvegarde et chargement des données avec pickle
with open("out.pkl", "wb") as f:
    pickle.dump(corpus_plus100, f)

with open("out.pkl", "rb") as f:
    corpus_plus100 = pickle.load(f)


##########################################Création du DataFrame à partir des infos récupérées########################
data = {
    'Identifiant': range(1, len(corpus_plus100) + 1),
    'Texte': corpus_plus100,
    'Origine': ['Reddit' if i < len(textes_Reddit) else 'Arxiv' for i in range(len(corpus_plus100))]
}

df = pd.DataFrame(data)

# Sauvegarde du DataFrame au format CSV
csv_file_path = 'fichier_du_corpus.csv'
df.to_csv(csv_file_path, sep='\t', index=False)

#Chargement du DataFrame avec le fichier CSV
loaded_df = pd.read_csv(csv_file_path, sep='\t')

# Affichage du DataFrame chargé
print(loaded_df.head())

# Affichage du temps actuel
aujourdhui = datetime.datetime.now()
print(aujourdhui)
