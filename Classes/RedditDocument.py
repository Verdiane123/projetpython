# Importing the Document class from the existing code
import ipywidgets as widgets
import Document, Author

# Partie 1

# Define the RedditDocument class as a subclass of Document
class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", nbre_commentaire=0):
        # Call the constructor of the parent class (Document)
        super().__init__(titre, auteur, date, url, texte)
        # Add the new field specific to Reddit
        self.nbre_commentaire = nbre_commentaire

    # Accessor and mutator for the nbre_commentaire field
    def get_nbre_commentaire(self):
        return self.nbre_commentaire

    def set_nbre_commentaire(self, nbre_commentaire):
        self.nbre_commentaire = nbre_commentaire

    # Override the __str__ method for custom display
    def __str__(self):
        return f"{super().__str__()}, Number of Comments: {self.nbre_commentaire}"
    
    def getType(self):
        return "Hello Reddit"
    
###################################################################################################
# Example usage:
# Create a RedditDocument instance
reddit_doc = RedditDocument(titre="Document Reddit TD 5", auteur="Verdiane", date="2023/11/23", url="https://www.reddit.com/sample", texte="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", nbre_commentaire=10)

# Display the RedditDocument instance
print(reddit_doc)
