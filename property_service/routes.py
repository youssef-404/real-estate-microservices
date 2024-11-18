from flask import Blueprint, request, jsonify, current_app
from property_service.models import Property, create_property, list_properties,get_property, update_property ,delete_property
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

property_blueprint = Blueprint('property', __name__)


@property_blueprint.route('/properties',methods=['POST'])
def add_property():
    client = current_app.config['DATASTORE_CLIENT']
    data = request.json

    # Transférer l'en-tête d'autorisation au user_service
    jwt_token = request.headers.get('Authorization')
    user_service_url = current_app.config['USER_SERVICE_URL']

    response = requests.get(f"{user_service_url}/users/validate",headers={"Authorization": jwt_token})
    if response.status_code != 200 or not response.json().get("valid"):
        return jsonify({"error": "Non autorisé."}), 401
    

    proprietaire = response.json()["user"]["id"]


    required_fields = ['nom','description','type_de_bien','ville']

    for field in required_fields :
        if field not in data :
            return jsonify({"error": f"Champ requis manquant : {field}"}),400
    

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
    client = current_app.config['DATASTORE_CLIENT']
    ville = request.args.get('city')

    if not ville:
        return jsonify({"error": "Vous devez spécifier une ville pour filtrer les propriétés."}),400
    
    filters = {'ville': ville}

    properties = list_properties(client, filters)
    return jsonify([{**dict(property), "id": property.key.id} for property in properties]), 200


@property_blueprint.route('/properties/<int:property_id>', methods =['GET'])
def get_property_by_id(property_id):
    client = current_app.config['DATASTORE_CLIENT']
    property_entity = get_property(client, property_id)

    if not property_entity:
        return jsonify({"error": "Propriété non trouvée."}), 404

    property_data = dict(property_entity)
    property_data["id"] = property_entity.key.id
    return jsonify(property_data), 200


@property_blueprint.route('/properties/<int:property_id>', methods=['PUT'])
def update_property_details(property_id):
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
