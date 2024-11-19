"""
Ce module définit les routes pour les opérations liées aux utilisateurs dans le service utilisateur.

Endpoints:
- POST /users: Enregistrer un nouvel utilisateur
- POST /login: Authentifier un utilisateur et fournir un JWT token.
- GET /users/<int:utilisateur_id>: Récupérer les détails d'un utilisateur (nécessite une authentification).
- PUT /users/<int:utilisateur_id>: Mettre à jour les détails d'un utilisateur (nécessite une authentification).
- DELETE /users/<int:utilisateur_id>: Supprimer un utilisateur (nécessite une authentification).
- GET /users/validate: Valider l'authentification de l'utilisateur actuel.

Dépendances :
- Flask pour la gestion des requêtes.
- SQLAlchemy pour les opérations sur la base de données.
- Flask-JWT-Extended pour l'authentification et la gestion des JWT.
"""


from flask import Blueprint, request, jsonify
from user_service.models import db, Utilisateur
from datetime import datetime
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity


# Définir un blueprint pour les routes liées aux utilisateurs
user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/users',methods=['POST'])
def register_user():
    """Enregistrer un nouvel utilisateur dans le système.
    
    Expects: 
        Une JSON avec 'email', 'password', 'nom', 'prenom' et 'date_de_naissance'.

    Returns:
        201 : Utilisateur enregistré avec succès.
        400 : Erreur de validation ou si l'utilisateur existe déjà.
    """
    data = request.json

    # Valider les champs requis
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

    # Hacher et définir le mot de passe de l'utilisateur
    new_utilisateur.set_password(data['password'])

    # Enregistrer l'utilisateur dans la base de données
    db.session.add(new_utilisateur)
    db.session.commit()

    return jsonify({"message": "Utilisateur enregistré avec succès.", "id": new_utilisateur.id}), 201



@user_blueprint.route('/login',methods=['POST'])
def login_user():
    """Authentifier un utilisateur et fournir un JWT token.

    Expects:
        Une JSON avec 'email' et 'password'.

    Returns:
        200 : JWT token pour des identifiants valides.
        400 : Identifiants manquants.
        401 : Identifiants invalides.
    """
    data = request.json

    # Valider les champs requis
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "L'email et le mot de passe sont obligatoires."}), 400
    
    # Récupérer l'utilisateur depuis la base de données
    utilisateur = Utilisateur.query.filter_by(email=data['email']).first()

    # Valider le mot de passe
    if not utilisateur or not utilisateur.check_password(data['password']):
        return jsonify({"error": "Identifiants invalides."}),401
    
    # Générer un token 
    token = create_access_token(identity=str(utilisateur.id))

    return jsonify({"token": token}), 200


@user_blueprint.route('/users/<int:utilisateur_id>',methods=['GET'])
@jwt_required()
def get_user(utilisateur_id):
    """Récupérer les détails d'un utilisateur par son ID.

    Requires:
        Authentification via JWT.

    Returns:
        200 : Détails de l'utilisateur authentifié.
        403 : Accès refusé si l'utilisateur tente d'accéder aux détails d'un autre utilisateur.
        404 : Utilisateur non trouvé.
    """

    current_utilisateur_id = get_jwt_identity()
    current_utilisateur_id = int(current_utilisateur_id)

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


@user_blueprint.route('/users/<int:utilisateur_id>', methods=['PUT'])
@jwt_required()
def update_user(utilisateur_id):
    """Mettre à jour les détails d'un utilisateur.

    Requires :
        Authentification via JWT.

    Expects :
    Une JSON avec les champs à mettre à jour ('nom', 'prenom', 'date_de_naissance').

    Returns :
        200 : Utilisateur mis à jour avec succès.
        403 : Accès refusé si l'utilisateur tente de mettre à jour les détails d'un autre utilisateur.
        404 : Utilisateur non trouvé.
    """

    current_utilisateur_id = get_jwt_identity()
    current_utilisateur_id = int(current_utilisateur_id)

    # l'utilisateur connecté ne peut récupérer que ses propres informations.
    if utilisateur_id != current_utilisateur_id:
        return jsonify({"error": "Accès refusé."}), 403
    
    utilisateur = db.session.get(Utilisateur,utilisateur_id)

    if not utilisateur:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Mettre à jour les champs si fournis
    data = request.json
    if data.get('nom'):
        utilisateur.nom = data['nom']
    if data.get('prenom'):
        utilisateur.prenom = data['prenom']
    if data.get('date_de_naissance'):
        utilisateur.date_de_naissance = data['date_de_naissance']

    db.session.commit()
    return jsonify({"message": "Utilisateur mis à jour avec succès."}), 200




@user_blueprint.route('/users/<int:utilisateur_id>', methods=['DELETE'])
@jwt_required()
def delete_user(utilisateur_id):
    """Supprimer un utilisateur par son ID.

    Requires:
            Authentification via JWT.

    Returns:
        200 : Utilisateur supprimé avec succès.
        403 : Accès refusé si l'utilisateur tente de supprimer le compte d'un autre utilisateur.
        404 : Utilisateur non trouvé.
    """
    current_utilisateur_id = get_jwt_identity()
    current_utilisateur_id = int(current_utilisateur_id)

    # l'utilisateur connecté ne peut récupérer que ses propres informations.
    if utilisateur_id != current_utilisateur_id:
        return jsonify({"error": "Accès refusé."}), 403
    
    utilisateur = db.session.get(Utilisateur,utilisateur_id)

    if not utilisateur:
        return jsonify({"error": "Utilisateur non trouvé."}), 404


    db.session.delete(utilisateur)
    db.session.commit()

    return jsonify({"message": "Utilisateur supprimé avec succès."}), 200




@user_blueprint.route('/users/validate', methods=['GET'])
@jwt_required()
def validate_user():
    """Valider l'authentification de l'utilisateur actuel.

    Requires:
        Authentification via JWT.

    Returns:
        200 : Détails de la validation de l'utilisateur.
        404 : Utilisateur non trouvé.
    """
     
    # Extraire l'ID utilisateur du JWT
    utilisateur_id = get_jwt_identity()
    utilisateur_id = int(utilisateur_id)

    utilisateur = db.session.get(Utilisateur,utilisateur_id)

    if not utilisateur:
        return jsonify({"valid": False, "error": "Utilisateur non trouvé."}), 404

    # Retourner les détails de l'utilisateur si valide
    return jsonify({
        "valid": True,
        "user": {
            "id": utilisateur.id,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "date_de_naissance": utilisateur.date_de_naissance,
            "email": utilisateur.email
        }
    }), 200

