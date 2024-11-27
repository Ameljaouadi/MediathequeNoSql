from flask import Blueprint, request, jsonify

from pymongo import MongoClient

# Configuration MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mediaDB']

# Créer un Blueprint pour les routes
abonne_bp = Blueprint('abonne', __name__)

@app.route('/AddAbonnee', methods=['POST'])
def create_abonne():
      data = {
        "nom": request.form.get("nom"),
        "prenom": request.form.get("prenom"),
        "email": request.form.get("email"),
        "adresse": request.form.get("adresse"),
        "liste_emprunt_cours": request.form.get("liste_emprunt_cours"),
        "historique_emprunt": request.form.get("historique_emprunt"),
        "date_inscription": request.form.get("date_inscription")
    }

    # Validation des données
    if not data["email"]:
        return jsonify({"error": "L'email est requis."}), 400
    # Vérifier si l'email existe déjà
    existing_abonne = db.abonne.find_one({"email": data["email"]})
    if existing_abonne:
        return jsonify({"error": "Un abonné avec cet email existe déjà."}), 409
   
  
    # Insérer le nouvel abonné si non existant
    db.abonne.insert_one(data)
    return redirect(url_for('Abonnees'))  # Rediriger vers la page des abonnés après l'ajout


@abonne_bp.route('/abonne', methods=['GET'])
def get_abonnes():
    abonnes = list(db.abonne.find({}, {"_id": 0}))
    return jsonify(abonnes), 200

@abonne_bp.route('/abonne/<email>', methods=['PUT'])
def update_abonne(email):
    # Récupérer les données JSON envoyées dans la requête
    data = request.json

    if not data:
        return jsonify({"error": "Aucune donnée fournie pour la mise à jour"}), 400

    # Validation des données : suppression des clés vides
    valid_data = {key: value for key, value in data.items() if value is not None and value != ""}

    if not valid_data:
        return jsonify({"error": "Aucun champ valide fourni pour la mise à jour"}), 400

    # Mise à jour des champs dans MongoDB
    result = db.abonne.update_one({"email": email}, {"$set": valid_data})

    # Vérifiez si un document a été trouvé et mis à jour
    if result.matched_count == 0:
        return jsonify({"error": f"Aucun abonné trouvé avec l'email '{email}'"}), 404

    if result.modified_count == 0:
        return jsonify({"message": "Aucun changement détecté dans les données"}), 200

    return jsonify({"message": "Abonné mis à jour avec succès !"}), 200


@abonne_bp.route('/abonne/<email>', methods=['DELETE'])
def delete_abonne(email):
    db.abonne.delete_one({"email": email})
    return jsonify({"message": "Abonné supprimé avec succès !"}), 200



# Routes pour Documents

# @main.route('/documents', methods=['POST'])
# def add_document():
#     data = request.json
#     document = {
#         'title': data['title'],
#         'author': data['author'],
#         'genre': data['genre'],
#         'available': data['available'],
#         'date_added': datetime.now()
#     }
#     db.documents.insert_one(document)
#     return jsonify({"message": "Document ajouté avec succès"}), 201


# @main.route('/documents/<title>', methods=['GET'])
# def get_document(title):
#     document = db.documents.find_one({'title': title})
#     if not document:
#         return jsonify({"message": "Document non trouvé"}), 404
#     document['_id'] = str(document['_id'])  # Convertir ObjectId en string
#     return jsonify(document)


# @main.route('/documents/<title>/availability', methods=['PUT'])
# def update_document_availability(title):
#     data = request.json
#     available = data.get('available')
#     result = db.documents.update_one({'title': title}, {'$set': {'available': available}})
#     if result.matched_count == 0:
#         return jsonify({"message": "Document non trouvé"}), 404
#     return jsonify({"message": "Disponibilité mise à jour avec succès"}), 200


# Routes pour Loans

# @main.route('/loans', methods=['POST'])
# def add_loan():
#     data = request.json
#     loan = {
#         'subscriber_email': data['subscriber_email'],
#         'document_title': data['document_title'],
#         'loan_date': datetime.strptime(data['loan_date'], "%Y-%m-%d"),
#         'return_date': data.get('return_date')
#     }
#     db.loans.insert_one(loan)
#     return jsonify({"message": "Emprunt ajouté avec succès"}), 201


# @main.route('/loans/<email>', methods=['GET'])
# def get_loans_by_email(email):
#     loans = db.loans.find({'subscriber_email': email})
#     result = []
#     for loan in loans:
#         loan['_id'] = str(loan['_id'])  # Convertir ObjectId en string
#         result.append(loan)
#     return jsonify(result)


# @main.route('/loans/return', methods=['PUT'])
# def mark_loan_returned():
#     data = request.json
#     result = db.loans.update_one(
#         {'subscriber_email': data['subscriber_email'], 'document_title': data['document_title']},
#         {'$set': {'return_date': datetime.now()}}
#     )
#     if result.matched_count == 0:
#         return jsonify({"message": "Emprunt non trouvé"}), 404
#     return jsonify({"message": "Document marqué comme retourné"}), 200
