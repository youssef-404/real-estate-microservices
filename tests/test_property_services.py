import pytest
from property_service.app import app
from unittest.mock import patch
from flask_jwt_extended import create_access_token
import json


class MockKey:
    def __init__(self, id):
        self.id = id

class MockProperty(dict):
    def __init__(self, data, id):
            super().__init__(data)
            self._data = data
            self.key = MockKey(id)

    def __getitem__(self, item):
            return self._data[item]

    def __iter__(self):
            return iter(self._data)

    def items(self):
            return self._data.items()


@pytest.fixture
def client():
    app.config['TESTING']= True
    
    with app.test_client() as client: 
        yield client


def test_create_property(client):
    with app.app_context():  # Assure app context pour create_access_token
        token = create_access_token(identity=2)
   
    # Simuler la fonction `create_property` utilisée dans la route
    with patch('property_service.routes.create_property') as mock_create_property :
        # Simuler la valeur de retour de `create_property`
        mock_create_property.return_value = mock_entity = type('MockEntity', (), {'id': 123456789})
    
        # En-tête d'autorisation
        headers = {'Authorization' : f'Bearer {token}'}

        payload = {
            "nom": "Villa Paradis",
            "description": "Superbe villa avec piscine et jardin tropical.",
            "type_de_bien": "Maison individuelle",
            "ville": "Nice",
            "pieces": [
                {
                "nom": "Salon",
                "surface": 35,
                "etage": "Rez-de-chaussée",
                "caracteristiques": ["Cheminée", "Accès terrasse"]
                },
                {
                "nom": "Cuisine",
                "surface": 20,
                "etage": "Rez-de-chaussée",
                "caracteristiques": ["Cuisine équipée", "Îlot central"]
                },
            ]
        }
        response = client.post('/properties',headers=headers,json=payload)

        assert response.status_code == 201
        assert response.json == {"id":123456789,"message":"Propriété créée avec succès."}

        # Vérifiez que la fonction simulée `create_property` a été appelée avec les arguments corrects
        mock_create_property.assert_called_once()


def test_get_property(client):
    with patch('property_service.routes.get_property') as mock_get_property:
        mock_get_property.return_value = MockProperty(
                {
                    "nom": "Villa Paradis",
                    "description": "Superbe villa avec piscine et jardin tropical.",
                    "type_de_bien": "Maison individuelle",
                    "ville": "Nice",
                    "proprietaire": "2",
                },
                id=123456789
            )
         
        response = client.get('/properties/123456789')

        assert response.status_code == 200
        assert response.json['nom'] == "Villa Paradis"
        assert response.json['id'] == 123456789
        mock_get_property.assert_called_once()




def test_list_properties_by_city(client):


    with patch('property_service.routes.list_properties') as mock_list_properties:
        mock_list_properties.return_value = [
            MockProperty(
                {
                    "nom": "Villa Paradis",
                    "description": "Superbe villa avec piscine et jardin tropical.",
                    "type_de_bien": "Maison individuelle",
                    "ville": "Nice",
                    "proprietaire": "2",
                },
                id=123456789
            ),
            MockProperty(
                {
                    "nom": "Appartement Vue Mer",
                    "description": "Appartement moderne avec balcon et vue sur la mer.",
                    "type_de_bien": "Appartement",
                    "ville": "Nice",
                    "proprietaire": "3",
                },
                id=987654321
            ),
        ]

        response = client.get('/properties?city=Nice')

        assert response.status_code == 200
     


def test_update_property(client):
    with app.app_context():
        token = create_access_token(identity="2")

    with patch('property_service.routes.get_property') as mock_get_property, \
         patch('property_service.routes.update_property') as mock_update_property:

        mock_get_property.return_value = MockProperty(
            {
                "nom": "Villa Paradis",
                "description": "Superbe villa avec piscine et jardin tropical.",
                "type_de_bien": "Maison individuelle",
                "ville": "Nice",
                "proprietaire": "2",
            },
            id=123456789
        )

        mock_update_property.return_value = MockProperty(
            {
                "nom": "Updated Villa Paradis",
                "description": "Superbe villa avec piscine et jardin tropical.",
                "type_de_bien": "Maison individuelle",
                "ville": "Nice",
                "proprietaire": "2",
            },
            id=123456789
        )


        headers = {'Authorization': f'Bearer {token}'}

        payload = {"nom": "Updated Villa Paradis"}
        
        response = client.put('/properties/123456789', headers=headers, json=payload)

        assert response.status_code == 200
        assert response.json == {"message": "Propriété mise à jour avec succès."}
        mock_update_property.assert_called_once()

    


def test_delete_property(client):
    with app.app_context():
        token = create_access_token(identity="2")

    with patch('property_service.routes.get_property') as mock_get_property, \
         patch('property_service.routes.delete_property') as mock_delete_property:

        mock_get_property.return_value = MockProperty(
            {
                "nom": "Villa Paradis",
                "description": "Superbe villa avec piscine et jardin tropical.",
                "type_de_bien": "Maison individuelle",
                "ville": "Nice",
                "proprietaire": "2",
            },
            id=123456789
        )

        mock_delete_property.return_value = True

        headers = {'Authorization': f'Bearer {token}'}

        response = client.delete('/properties/123456789', headers=headers)

     
        assert response.status_code == 200
        assert response.json == {"message": "Propriété supprimée avec succès."}

        mock_delete_property.assert_called_once()
