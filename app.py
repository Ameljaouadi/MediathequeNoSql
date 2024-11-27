from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient


app = Flask(__name__,static_folder='FrontEnd/Static',template_folder='FrontEnd/Templates')

client = MongoClient("mongodb://localhost:27017/")
db = client["mediaDB"]



@app.route('/SideBar')
def sidebar():
    return render_template('SideBar.html')

@app.route('/NavBar')
def navbar():
    return render_template('NavBar.html')

@app.route('/AddAbonnee', methods=['GET', 'POST'])
def addAbonnees():
    if request.method == 'POST':
        # Collecting data from the form
        data = {
            "nom": request.form.get("nom"),
            "prenom": request.form.get("prenom"),
            "email": request.form.get("email"),
            "adresse": request.form.get("adresse"),
            "liste_emprunt_cours": request.form.get("liste_emprunt_cours"),
            "historique_emprunt": request.form.get("historique_emprunt"),
            "date_inscription": request.form.get("date_inscription")
        }
        
        # Insert data into the MongoDB collection
        db.abonne.insert_one(data)
        
        # Redirect to the abonnes page after successfully adding the abonne
        return redirect(url_for('abonnees'))
    
    # If it's a GET request, just render the form
    return render_template('AddAbonnee.html')

@app.route('/abonnees')
def abonnees():
    abonnes = list(db.abonne.find({}, {"_id": 0})) 
    return render_template('Abonnees.html', abonnes=abonnes) 


@app.route('/delete_abonne/<email>', methods=['POST'])
def delete_abonne(email):
     # Tenter de supprimer l'abonné
    result = db.abonne.delete_one({"email": email})
    
    # Vérifier si l'abonné existait
    if result.deleted_count == 0:
        return "Aucun abonné trouvé avec cet email.", 404

    # Rediriger vers la liste des abonnés après suppression
    return redirect(url_for('abonnees'))
@app.route('/catalogues')
def catalogues():
    return render_template('Catalogue.html') 

@app.route('/emprunts')
def emprunts():
    return render_template('Emprunts.html') 

@app.route('/')
def Dashbord():
    return render_template('Dashbord.html') 
if __name__ == "__main__":
    app.run(debug=True)