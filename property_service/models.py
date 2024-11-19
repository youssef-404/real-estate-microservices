"""
Ce module gère les opérations CRUD (Créer, Lire, Mettre à jour, Supprimer) 
pour les propriétés à l'aide de Google Cloud Datastore.

Contenu:
- Définition du modèle `Property` avec dataclasses.
- Fonctions utilitaires pour interagir avec Google Datastore, y compris :
  - Création de propriétés.
  - Liste des propriétés avec filtres.
  - Récupération d'une propriété par son identifiant.
  - Mise à jour et suppression des propriétés.
"""


from google.cloud import datastore
from dataclasses import dataclass, asdict

@dataclass
class Property:
    """Représentation d'une propriété immobilière.

    Attributs:
        - nom (str): Nom de la propriété.
        - description (str): Description de la propriété.
        - type_de_bien (str): Type de bien .
        - ville (str): Ville où se trouve la propriété.
        - proprietaire (int): Identifiant du propriétaire.
        - pieces (list): Liste des pièces et leurs caractéristiques (facultatif).
    """
    nom : str
    description : str
    type_de_bien : str
    ville : str 
    proprietaire : int
    pieces : list = None


def create_property(client,property_data):
    """Crée une nouvelle propriété dans Datastore.

    Paramètres:
        - client (datastore.Client): Client Google Datastore.
        - property_data (Property): Objet de type `Property` contenant les données de la propriété.

    Retourne:
        - entity (datastore.Entity): Entité nouvellement créée dans Datastore.
    """

    # Génère une clé pour une nouvelle entité de type "Property"
    key = client.key('Property')
    entity = datastore.Entity(key=key)
    entity.update(asdict(property_data))

    # Enregistre l'entité dans Datastore
    client.put(entity)

    return entity



def list_properties(client, filters=None):
    """Récupère la liste des propriétés avec des filtres facultatifs.

    Paramètres:
        - client (datastore.Client): Client Google Datastore.
        - filters (dict): Dictionnaire de filtres (ex: {"ville": "Paris"}).

    Retourne:
        - List[datastore.Entity]: Liste des entités correspondant aux critères.
    """

    query = client.query(kind='Property')

    if filters:
        for field, value in filters.items():
            query.add_filter(field, '=', value) # Ajoute des filtres à la requête

    return list(query.fetch())



def get_property(client, property_id):
    """Récupère une propriété spécifique par son identifiant.

    Paramètres:
        - client (datastore.Client): Client Google Datastore.
        - property_id (int): Identifiant unique de la propriété.

    Retourne:
        - datastore.Entity ou None: L'entité si trouvée, sinon None.
    """
    key= client.key('Property',property_id)

    return client.get(key)



def update_property(client, property_id, updates):
    """ Met à jour une propriété existante avec les nouvelles données.

    Paramètres:
        - client (datastore.Client): Client Google Datastore.
        - property_id (int): Identifiant unique de la propriété à mettre à jour.
        - updates (dict): Dictionnaire contenant les champs à mettre à jour.

    Retourne:
        - entity (datastore.Entity) ou None: L'entité mise à jour si trouvée, sinon None.
    """

    key = client.key('Property', property_id)
    entity = client.get(key)
    
    # Propriété non trouvée
    if not entity:
        return None  
    
    entity.update(updates) # Met à jour les champs avec les nouvelles données
    client.put(entity) # Enregistre les modifications dans Datastore

    return entity



def delete_property(client, property_id):
    """Supprime une propriété existante par son identifiant.

    Paramètres:
        - client (datastore.Client): Client Google Datastore.
        - property_id (int): Identifiant unique de la propriété à supprimer.

    Retourne:
        - None
    """
    key = client.key('Property', property_id)
    client.delete(key)