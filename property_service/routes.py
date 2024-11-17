from flask import Blueprint, request, jsonify, current_app
from property_service.models import Property, create_property, list_properties,get_property, update_property ,delete_property
from flask_jwt_extended import jwt_required, get_jwt_identity

property_blueprint = Blueprint('property', __name__)


@property_blueprint.route('/properties',methods=['POST'])
@jwt_required()
def add_property():
    client = current_app.config['DATASTORE_CLIENT']
    data = request.json

    required_fields = ['nom','description','type_de_bien','ville']

    for field in required_fields :
        if field not in data :
            return jsonify({"error": f"Champ requis manquant : {field}"}),400
    

    data['proprietaire'] = get_jwt_identity()

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

    return jsonify(dict(property_entity)), 200


@property_blueprint.route('/properties/<int:property_id>', methods=['PUT'])
@jwt_required()
def update_property_details(property_id):
    client = current_app.config['DATASTORE_CLIENT']
    data = request.json

    property_entity = get_property(client, property_id)
    if not property_entity:
        return jsonify({"error": "Propriété non trouvée."}), 404
    
    # Valider la propriété
    proprietaire = get_jwt_identity()
    if property_entity.get('proprietaire') != proprietaire:
        return jsonify({"error": "Vous n'êtes pas autorisé à mettre à jour cette propriété."}), 403


    update_property(client, property_id, data)


    return jsonify({"message": "Propriété mise à jour avec succès."}), 200


@property_blueprint.route('/properties/<int:property_id>', methods=['DELETE'])
@jwt_required()
def delete_property_details(property_id):
    client = current_app.config['DATASTORE_CLIENT']

    property_entity = get_property(client, property_id)
    if not property_entity:
        return jsonify({"error": "Propriété non trouvée."}), 404
    
    # Valider la propriété
    proprietaire = get_jwt_identity()
    if property_entity.get('proprietaire') != proprietaire:
        return jsonify({"error": "Vous n'êtes pas autorisé à supprimer cette propriété."}), 403

    delete_property(client, property_id)

    return jsonify({"message": "Propriété supprimée avec succès."}), 200
