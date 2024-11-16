from flask import Blueprint, request, jsonify
from models import db, Utilisateur
from datetime import datetime
from flask_jwt_extended import create_access_token


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
