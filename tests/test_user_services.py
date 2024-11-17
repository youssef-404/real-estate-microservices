import pytest
from user_service.app import app,db


@pytest.fixture
def client():
    app.config['TESTING']= True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.drop_all() 
            db.create_all()
        
        yield client


def test_register_user(client):
    response = client.post('/users', json={
        "email": "email@gmail.com",
        "password": "password",
        "nom": "nom",  
        "prenom": "prenom",
        "date_de_naissance": "2001-04-10"  
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["message"] == "Utilisateur enregistré avec succès."


def test_login_user(client):
    # Enregistrer un utilisateur
    client.post('/users', json={
        "email": "email@gmail.com",
        "password": "password",
        "nom": "nom",  
        "prenom": "prenom",
        "date_de_naissance": "2001-04-10"  
    })
    
    # Se connecter avec des identifiants corrects
    response = client.post('/login',json={
        "email": "email@gmail.com",
        "password": "password",
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


    # Se connecter avec des identifiants incorrects
    response = client.post('/login', json={
        "email": "email@gmail.com",
        "password": "passworf",
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Identifiants invalides.'


def test_get_user(client):
    # Enregistrer un utilisateur
    client.post('/users', json={
        "email": "email@gmail.com",
        "password": "password",
        "nom": "nom",  
        "prenom": "prenom",
        "date_de_naissance": "2001-04-10"    
    })

    response = client.post('/login', json={
        "email": "email@gmail.com",
        "password": "password",
    })

    token = response.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Tester GET /users/<id>
    response = client.get('/users/1', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == 'email@gmail.com'



def test_put_user(client):
    # Enregistrer un utilisateur
    client.post('/users', json={
        "email": "email@gmail.com",
        "password": "password",
        "nom": "nom",  
        "prenom": "prenom",
        "date_de_naissance": "2001-04-10"  
    })

    response = client.post('/login', json={
        "email": "email@gmail.com",
        "password": "password",
    })

    token = response.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Tester PUT /users/<id>
    response = client.put('/users/1',json={'nom':'nom2'}, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Utilisateur mis à jour avec succès.'



def test_delete_user(client):
    # Enregistrer un utilisateur
    client.post('/users', json={
        "email": "email@gmail.com",
        "password": "password",
        "nom": "nom",  
        "prenom": "prenom",
        "date_de_naissance": "2001-04-10"    
    })

    response = client.post('/login', json={
        "email": "email@gmail.com",
        "password": "password",
    })

    token = response.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Tester DELETE /users/<id>
    response = client.delete('/users/1', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Utilisateur supprimé avec succès.'




def test_unauthorized_user(client):
    # Enregistrer un utilisateur
    client.post('/users', json={
        "email": "email@gmail.com",
        "password": "password",
        "nom": "nom",  
        "prenom": "prenom",
        "date_de_naissance": "2001-04-10"    
    })

    client.post('/users', json={
        "email": "email2@gmail.com",
        "password": "password2",
        "nom": "nom2",  
        "prenom": "prenom2",
        "date_de_naissance": "2001-04-19"    
    })


    response = client.post('/login', json={
        "email": "email@gmail.com",
        "password": "password",
    })


    token = response.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Tester l'accès non autorisé
    response = client.delete('/users/2', headers=headers)
    assert response.status_code == 403
    data = response.get_json()
    assert data['error'] == 'Accès refusé.'