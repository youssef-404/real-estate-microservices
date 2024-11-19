"""
Fichier contenant les routes pour le service des propriétés.

Ce fichier définit les routes pour les opérations CRUD (Créer, Lire, Mettre à jour, Supprimer) 
sur les propriétés. Il utilise Google Cloud Datastore comme base de données et valide 
les utilisateurs via des appels au service utilisateur (user_service).

Les routes incluent :
- Création de propriétés
- Liste des propriétés filtrées par ville
- Récupération d'une propriété par ID
- Mise à jour et suppression de propriétés (avec validation de l'utilisateur)
"""

from flask import Blueprint, request, jsonify, current_app
from property_service.models import Property, create_property, list_properties,get_property, update_property ,delete_property
import requests


# Définition du blueprint pour les routes des propriétés
property_blueprint = Blueprint('property', __name__)


@property_blueprint.route('/properties',methods=['POST'])
def add_property():
    """ Crée une nouvelle propriété dans Datastore après validation de l'utilisateur.
    
    Étapes :
        1. Valider l'utilisateur via user_service.
        2. Vérifier que tous les champs obligatoires sont présents.
        3. Enregistrer la propriété dans Datastore.

    Retourne:
        - 201: Propriété créée avec succès.
        - 400: Champs requis manquants.
        - 401: Utilisateur non autorisé.
    """

    client = current_app.config['DATASTORE_CLIENT']
    data = request.json

    # Transférer l'en-tête d'autorisation au user_service
    jwt_token = request.headers.get('Authorization')
    user_service_url = current_app.config['USER_SERVICE_URL']

    response = requests.get(f"{user_service_url}/users/validate",headers={"Authorization": jwt_token})
    if response.status_code != 200 or not response.json().get("valid"):
        return jsonify({"error": "Non autorisé."}), 401
    
    # Récupérer l'ID de l'utilisateur validé
    proprietaire = response.json()["user"]["id"]


    required_fields = ['nom','description','type_de_bien','ville']

    for field in required_fields :
        if field not in data :
            return jsonify({"error": f"Champ requis manquant : {field}"}),400
    
    # Ajouter le propriétaire à la propriété
    data['proprietaire'] = proprietaire

    # Créer un objet Propriété
    property_data = Property(
        nom=data['nom'],
        description=data['description'],
        type_de_bien=data['type_de_bien'],
        ville=data['ville'],
        proprietaire=data['proprietaire'],
        pieces=data.get('pieces', [])
    )

    # Enregistrer dans Datastore
    entity = create_property(client, property_data)
    return jsonify({"id": entity.id, "message": "Propriété créée avec succès."}), 201


@property_blueprint.route('/properties', methods=['GET'])
def list_all_properties():
    """Liste toutes les propriétés dans une ville spécifique.

    Paramètre de requête:
        - city: Nom de la ville pour filtrer les propriétés.

    Retourne:
        - 200: Liste des propriétés.
        - 400: Si le paramètre de ville est manquant.
    """

    client = current_app.config['DATASTORE_CLIENT']
    ville = request.args.get('city')

    if not ville:
        return jsonify({"error": "Vous devez spécifier une ville pour filtrer les propriétés."}),400
    
    filters = {'ville': ville}

    properties = list_properties(client, filters)
    return jsonify([{**dict(property), "id": property.key.id} for property in properties]), 200


@property_blueprint.route('/properties/<int:property_id>', methods =['GET'])
def get_property_by_id(property_id):
    """Récupère les détails d'une propriété spécifique par son identifiant.

    Paramètres:
        - property_id: Identifiant unique de la propriété.

    Retourne:
        - 200: Détails de la propriété.
        - 404: Si la propriété n'existe pas.
    """
    client = current_app.config['DATASTORE_CLIENT']
    property_entity = get_property(client, property_id)

    if not property_entity:
        return jsonify({"error": "Propriété non trouvée."}), 404

    # Ajouter l'ID de la propriété au résultat
    property_data = dict(property_entity)
    property_data["id"] = property_entity.key.id
    return jsonify(property_data), 200


@property_blueprint.route('/properties/<int:property_id>', methods=['PUT'])
def update_property_details(property_id):
    """Met à jour les détails d'une propriété après validation de l'utilisateur.

    Paramètres:
        - property_id: Identifiant de la propriété.

    Retourne:
        - 200: Propriété mise à jour.
        - 403: Si l'utilisateur n'est pas le propriétaire.
        - 404: Si la propriété n'existe pas.
    """
    client = current_app.config['DATASTORE_CLIENT']
    data = request.json

    # Transférer l'en-tête d'autorisation au user_service
    jwt_token = request.headers.get('Authorization')
    user_service_url = current_app.config['USER_SERVICE_URL']

    response = requests.get(f"{user_service_url}/users/validate",headers={"Authorization": jwt_token})
    if response.status_code != 200 or not response.json().get("valid"):
        return jsonify({"error": "Non autorisé."}), 401
  

    property_entity = get_property(client, property_id)
    if not property_entity:
        return jsonify({"error": "Propriété non trouvée."}), 404
    
    proprietaire = response.json()["user"]["id"]

    # Valider la propriété
    if property_entity.get('proprietaire') != proprietaire:
        return jsonify({"error": "Vous n'êtes pas autorisé à mettre à jour cette propriété."}), 403


    update_property(client, property_id, data)


    return jsonify({"message": "Propriété mise à jour avec succès."}), 200


@property_blueprint.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property_details(property_id):
    """Supprime une propriété après validation de l'utilisateur.

    Paramètres:
        - property_id: Identifiant de la propriété.

    Retourne:
        - 200: Propriété supprimée.
        - 403: Si l'utilisateur n'est pas le propriétaire.
        - 404: Si la propriété n'existe pas.
    """
    client = current_app.config['DATASTORE_CLIENT']

    # Transférer l'en-tête d'autorisation au user_service
    jwt_token = request.headers.get('Authorization')
    user_service_url = current_app.config['USER_SERVICE_URL']

    response = requests.get(f"{user_service_url}/users/validate",headers={"Authorization": jwt_token})
    if response.status_code != 200 or not response.json().get("valid"):
        return jsonify({"error": "Non autorisé."}), 401
  

    property_entity = get_property(client, property_id)
    if not property_entity:
        return jsonify({"error": "Propriété non trouvée."}), 404
    
    proprietaire = response.json()["user"]["id"]

    # Valider la propriété
    if property_entity.get('proprietaire') != proprietaire:
        return jsonify({"error": "Vous n'êtes pas autorisé à supprimer cette propriété."}), 403

    delete_property(client, property_id)

    return jsonify({"message": "Propriété supprimée avec succès."}), 200
