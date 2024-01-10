#Création de la classe Document
class Document:
    def __init__(self, titre="",auteur="",date="",texte="", type = ""):
      self.titre = titre
      self.auteur = auteur
      self.date = date
      self.texte = texte
      self.type = type

    #Afficher toutes les informations d'une instance
    def __affiche__(self):
      return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.texte}"

    def __str__(self):
       return f"Titre : {self.titre}"

#Classe fille Reddit
class RedditDocument(Document):
  def __init__(self, titre="", auteur="", date="", texte="", nbCommentaires="", type  = ""):
      super().__init__(titre, auteur, date, texte, type)
      self.ncommentaires = nbCommentaires
  
  #Getters et Setters
  def getTitre(self):
     return self.titre
  def setTitre(self, titre):
     self.titre = titre

  def getAuteur(self):
     return self.auteur
  def setAuteur(self, auteur):
     self.auteur = auteur

  def getDate(self):
     return self.date
  def setDate(self, date):
     self.date =date

  def getTexte(self):
     return self.texte
  def setTexte(self, texte):
     self.texte = texte

  def getNbCommentaires(self):
     return self.ncommentaires
  def setNbCommentaires(self, nbCommentaires):
     self.ncommentaires = nbCommentaires

   #methode getType
  def getType(self):
     return self.type

  #Affichage digeste
  def __str__(self):
     return super().__str__()
     
#Classe fille Arxiv
class ArxivDocument(Document):
  def __init__(self, titre="", auteur="", date="", texte="", type = "",coAuteurs=""):
      super().__init__(titre, auteur, date, texte, type)
      self.coAuteurs = coAuteurs
  
  #Getters et Setters
  def getTitre(self):
     return self.titre
  def setTitre(self, titre):
     self.titre = titre

  def getAuteur(self):
     return self.auteur
  def setAuteur(self, auteur):
     self.auteur = auteur

  def getDate(self):
     return self.date
  def setDate(self, date):
     self.date =date

  def getTexte(self):
     return self.texte
  def setTexte(self, texte):
     self.texte = texte

  def getCoAuteurs(self):
     return self.coAuteurs
  def setNbCommentaires(self, coAuteurs):
     self.coAuteurs = coAuteurs
 
   #methode getType
  def getType(self):
     return self.type

  #Affichage digeste
  def __str__(self):
     return super().__str__()
