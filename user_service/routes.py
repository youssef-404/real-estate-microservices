from flask import Blueprint, request, jsonify
from user_service.models import db, Utilisateur
from datetime import datetime
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity


utilisateur_blueprint = Blueprint('utilisateur', __name__)


@utilisateur_blueprint.route('/users',methods=['POST'])
def register_user():
    data = request.json
    if not data.get('email') or not data.get('password') or not data.get('nom') or not data.get('prenom') or not data.get('date_de_naissance'):
        return jsonify({"error": "Tous les champs sont obligatoires."}), 400
    
    # Vérifiez si l'utilisateur existe déjà
    if Utilisateur.query.filter_by(email=data['email']).first():
        return jsonify({"error":"L'utilisateur existe déjà"}), 400
    
    # Convertir date_de_naissance en un objet datetime.date
    data['date_de_naissance'] = datetime.strptime(data['date_de_naissance'], '%Y-%m-%d').date()

    # Créez et enregistrez l'utilisateur
    new_utilisateur = Utilisateur(
        email = data['email'],
        nom = data['nom'],
        prenom = data['prenom'],
        date_de_naissance =  data['date_de_naissance']
    )

    new_utilisateur.set_password(data['password'])
    db.session.add(new_utilisateur)
    db.session.commit()

    return jsonify({"message": "Utilisateur enregistré avec succès.", "id": new_utilisateur.id}), 201



@utilisateur_blueprint.route('/login',methods=['POST'])
def login_user():
    data = request.json
    
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "L'email et le mot de passe sont obligatoires."}), 400

    utilisateur = Utilisateur.query.filter_by(email=data['email']).first()

    if not utilisateur or not utilisateur.check_password(data['password']):
        return jsonify({"error": "Identifiants invalides."}),401
    
    token = create_access_token(identity=utilisateur.id)

    return jsonify({"token": token}), 200


@utilisateur_blueprint.route('/users/<int:utilisateur_id>',methods=['GET'])
@jwt_required()
def get_user(utilisateur_id):
    current_utilisateur_id = get_jwt_identity()

    # l'utilisateur connecté ne peut récupérer que ses propres informations.
    if utilisateur_id != current_utilisateur_id:
        return jsonify({"error": "Accès refusé."}), 403
    

    utilisateur = db.session.get(Utilisateur,utilisateur_id)

    if not utilisateur:
        return jsonify({"error":"Utilisateur non trouvé."}),404
    
    
    return jsonify({
        "id":utilisateur.id,
        "email":utilisateur.email,
        "nom":utilisateur.nom,
        "prenom":utilisateur.prenom,
        "date_de_naissance":utilisateur.date_de_naissance.isoformat()
    }),200


@utilisateur_blueprint.route('/users/<int:utilisateur_id>', methods=['PUT'])
@jwt_required()
def update_user(utilisateur_id):
    current_utilisateur_id = get_jwt_identity()
    
    # l'utilisateur connecté ne peut récupérer que ses propres informations.
    if utilisateur_id != current_utilisateur_id:
        return jsonify({"error": "Accès refusé."}), 403
    
    utilisateur = db.session.get(Utilisateur,utilisateur_id)

    if not utilisateur:
        return jsonify({"error": "Utilisateur non trouvé."}), 404


    data = request.json
    if data.get('nom'):
        utilisateur.nom = data['nom']
    if data.get('prenom'):
        utilisateur.prenom = data['prenom']
    if data.get('date_de_naissance'):
        utilisateur.date_de_naissance = data['date_de_naissance']

    db.session.commit()
    return jsonify({"message": "Utilisateur mis à jour avec succès."}), 200




@utilisateur_blueprint.route('/users/<int:utilisateur_id>', methods=['DELETE'])
@jwt_required()
def delete_user(utilisateur_id):
    current_utilisateur_id = get_jwt_identity()
    
    # l'utilisateur connecté ne peut récupérer que ses propres informations.
    if utilisateur_id != current_utilisateur_id:
        return jsonify({"error": "Accès refusé."}), 403
    
    utilisateur = db.session.get(Utilisateur,utilisateur_id)

    if not utilisateur:
        return jsonify({"error": "Utilisateur non trouvé."}), 404


    db.session.delete(utilisateur)
    db.session.commit()

    return jsonify({"message": "Utilisateur supprimé avec succès."}), 200


