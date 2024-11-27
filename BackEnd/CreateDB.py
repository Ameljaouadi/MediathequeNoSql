from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Specify the database name
db_name = "mediaDB"  
db = client[db_name]

# # Create a collection and insert a sample document
# #db.users.insert_one({"name": "amel", "email": "amel@gmail.com"})
# db.documents.insert_one({ 
#     "titre": "titanic", 
#     "type": "drama",
#      "auteur":"houyem",
#       "date_publication":"10/05/2014",
#        "disponibilite":"oui"})
# db.abonne.insert_one({
#     "nom": "maissa", 
    
#     "prenom": "daas", 
#     "adresse": "test", 
#     "date_inscription": "19/11/2024", 
#     "liste_emprunt_cours": "test", 
#     "historique_emprunt": "test"
# })
print(f"Database '{db_name}' created successfully with a sample document.")