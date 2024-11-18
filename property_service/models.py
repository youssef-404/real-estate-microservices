from google.cloud import datastore
from dataclasses import dataclass, asdict

@dataclass
class Property:
    nom : str
    description : str
    type_de_bien : str
    ville : str 
    proprietaire : str
    pieces : list = None


def create_property(client,property_data):
    key = client.key('Property')
    entity = datastore.Entity(key=key)
    entity.update(asdict(property_data))
    client.put(entity)

    return entity



def list_properties(client, filters=None):
    query = client.query(kind='Property')

    if filters:
        for field, value in filters.items():
            query.add_filter(field, '=', value)

    return list(query.fetch())



def get_property(client, property_id):
    key= client.key('Property',property_id)

    return client.get(key)



def update_property(client, property_id, updates):
    key = client.key('Property', property_id)
    entity = client.get(key)
    
    # Propriété non trouvée
    if not entity:
        return None  
    
    entity.update(updates)
    client.put(entity)

    return entity



def delete_property(client, property_id):
    key = client.key('Property', property_id)
    client.delete(key)