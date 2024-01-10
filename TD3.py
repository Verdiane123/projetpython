import praw
import urllib.request
import xmltodict
import numpy as np
import pandas as pd
from Document import *
import datetime
from Corpus import *
import pickle
from Author import Author

#-------Reddit------
# Paramétrage de l'accès à Reddit avec nos identifiants
reddit = praw.Reddit(client_id='XeGdTMC-rc43XE82RePFIA', client_secret='gOxGq7tbQm1MJ8MnstrkPAjoHyP4hw', user_agent='emma')

# Récupération des données (titre, textes, auteurs et années de parution) depuis Reddit sur la base de notre thématique : le FOOTBALL
subr = reddit.subreddit('Football')
titres_Reddit = []
textes_Reddit = []   
auteurs_Reddit = []  
annees_Reddit = []

for post in subr.hot(limit=100):
    titre = post.title
    #titre = titre.replace("\n", " ")
    titres_Reddit.append(titre)
    textes_Reddit.append(post.selftext.replace("\n", " ")) #c'était docs avant  
    auteurs_Reddit.append(post.author.name)  
    annees_Reddit.append(post.created_utc)

#-------Arxiv----------
# Récupération des données depuis ArXiv avec les mêmes options que Reddit
titres_Arxiv = []
textes_Arxiv = []
auteurs_Arxiv = []  
annees_Arxiv = []   
query = "football"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()
data = url_read.decode()
dico = xmltodict.parse(data)
clé = list(dico.keys())
#print(clé)
docs = dico['feed']['entry']


for d in docs:
    titre = d['title']
    titres_Arxiv.append(titre)
    texte = d['title'] + ". " + d['summary']
    texte = texte.replace("\n", " ")
    textes_Arxiv.append(texte)
    # Extraction des noms des auteurs
    auteurs = [a['name'] if isinstance(a, dict) and 'name' in a else a for a in d.get('author', [])]
    auteurs_Arxiv.append(auteurs)  #Liste
    annees_Arxiv.append(int(d['published'][:4]))  #extraction avec la clé 'published' pour Arvix


# Concaténation des textes (TD3)
corpus_v1 = textes_Reddit + textes_Arxiv

#---------------TD4---------------
# Création des collections sous forme de dictionnaire pour indexer les Documents et les Auteurs
id2doc = {}
id2aut = {}
index_document = 1

# Récupération des données depuis Reddit
for i, (titre, texte, auteur, annee) in enumerate(zip(titres_Reddit, textes_Reddit, auteurs_Reddit, annees_Reddit), start=index_document):
    ##Alimenter id2aut en ajoutant une instance d'Author à chaque fois qu'on a un nouvel auteur
    if auteur not in id2aut:
        id2aut[auteur] = Author(name=auteur)

    '''
    #Création d'un objet Document (TD4)
    doc = Document(
        titre=f"Document Reddit {i+1}",
        auteur=auteur,
        date=datetime.datetime.utcfromtimestamp(annee).strftime("%Y-%m-%d"),
        #url="",
        texte=texte
    )
    '''

    #Création d'un objet RedditDocument (Héritage TD5)
    doc = RedditDocument(
        titre=titre,
        auteur=auteur,
        date=datetime.datetime.utcfromtimestamp(annee).strftime("%Y-%m-%d"),
        #url="",
        texte=texte,
        type="Reddit"
    )

    # Mettre à jour des infos de l'auteur
    id2aut[auteur].add(doc)

    # Ajout de l'instance Document au dictionnaire id2doc
    id2doc[index_document] = doc
    index_document += 1

# Récupération des données depuis ArXiv
for i, (titre, texte, auteurs, annee) in enumerate(zip(titres_Arxiv, textes_Arxiv, auteurs_Arxiv, annees_Arxiv), start=index_document):
    #Alimenter id2aut en ajoutant une instance d'Author à chaque fois qu'on a un nouvel auteur
    if auteur not in id2aut:
        id2aut[auteur] = Author(name=auteur)
    '''
    #Création d'un objet Document (TD4)
    doc = Document(
        titre=f"Document ArXiv {i+1}",
        auteur=", ".join(auteurs),
        date=str(annee),
        #url="",
        texte=texte
    )
    '''
    
    #Création d'un objet ArxivDocument (Héritage TD5)
    doc = ArxivDocument(
        titre=f"Document ArXiv {i+1}",
        auteur=", ".join(auteurs),
        date=str(annee),
        #url="",
        texte=texte,
        type="Arxiv"
    )
    # Mise à jour
    id2aut[auteur].add(doc)

    id2doc[index_document] = doc
    index_document += 1


#Création du corpus
corpus = Corpus(nom="Le corpus")

#Ajout des documents au corpus
for i, doc in id2doc.items():
    corpus.add(doc)


#Affichage des documents triés par titre
print("Affichage des documents par titre:")
print(corpus.show(n_docs=5, tri="abc"))

#Affichage des documents triés par date
print("\nAffichage des documents par date:")
print(corpus.show(n_docs=5, tri="123"))

# Recherche de mots-clés dans le corpus   RECHERCHE DE MOT DANS LE CORPUS
#keyword = "football"
keyword = input("Entrez le mot-clé à rechercher : ")
occurence = corpus.search(keyword)
nombre_occurence = len(occurence)
print(f"\nNombre d'occurrences du mot-clé '{keyword}' dans le corpus : {nombre_occurence}")

# Utilisez la fonction concorde pour rechercher une expression avec un contexte     RECHERCHE D'EXPRESSION
expression_recherchee = input("Entrez l'expression à rechercher : ")
taille_contexte = 15
resultats_concorde = corpus.concorde(expression_recherchee, taille_contexte)

# Affichez les résultats de la concordance
print("\nRésultats de la concordance :")
print(resultats_concorde)

# Demander des statistiques d'un auteur RECHERCHE DES INFOS LIÉES AUX OEUVRES D'UN AUTEUR
requete_auteur = input("\nEntrez le nom de l'auteur recherché : ")
if requete_auteur in corpus.aut2id:
    statistique_auteur = corpus.authors[corpus.aut2id[requete_auteur]]
    print(f"Statistiques de {statistique_auteur.name}:")
    print(f"Nombre de documents publiés : {statistique_auteur.ndoc}")
    if statistique_auteur.ndoc > 0:
        taille_moyenne = np.mean([len(texte) for texte in statistique_auteur.production])
        print(f"Taille moyenne des documents : {taille_moyenne:.2f} caractères")
else:
    print(f"Désolé ! L'auteur {requete_auteur} n'est pas connu. 😕")

print(corpus.__repr__())
#test de stat
corpus.stats(5) 



''' ###TEST###
print(corpus.__repr__())
corpus.show(n_docs=5, tri="123")
corpus.save("C:/Users/cynth/OneDrive/Documents/Python/Projet python/out.pkl")
c = corpus.load("C:/Users/cynth/OneDrive/Documents/Python/Projet python/out.pkl")
c.show(5,"123")
'''

'''
#-----TD4--------
collection = []
for nature, doc in docs_bruts:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #showDictStruct(doc)

        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

        doc_classe = Document(titre, authors, date, summary)  # Création du Document
        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":
        #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        doc_classe = Document(titre, auteur, date, texte)

        collection.append(doc_classe)


# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre

#Traitement des auteurs
authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création de la liste+index des Auteurs
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)

'''