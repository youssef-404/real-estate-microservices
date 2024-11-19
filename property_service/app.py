"""
Fichier principal de l'application pour le service de gestion des propriétés.

Ce fichier configure et initialise l'application Flask, les extensions nécessaires et enregistre les routes pour les propriétés.

Points principaux :
- Chargement des variables d'environnement.
- Configuration de Google Datastore pour stocker les propriétés.
- Initialisation de Flask-JWT-Extended pour la gestion des JWT.
- Route de santé pour vérifier le bon fonctionnement de l'application.
"""


from flask import Flask
from google.cloud import datastore
from dotenv import load_dotenv
from property_service.routes import property_blueprint
import os

load_dotenv()

# Initialisation de l'application Flask
app = Flask(__name__)

# Charger le chemin des informations d'identification pour Google Datastore
credentials_path =os.getenv("DATASTORE_CREDENTIALS")
# URL du service utilisateur
app.config['USER_SERVICE_URL'] = os.getenv("USER_SERVICE_URL")
app.config['PORT'] = os.getenv("PORT",5001)


# Vérifier si les informations d'identification pour Google Datastore sont correctement définies
if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS n'est pas défini dans le fichier .env.")

# Initialisation du client Google Datastore avec le fichier d'identification JSON
app.config['DATASTORE_CLIENT'] = datastore.Client.from_service_account_json(credentials_path)

# Enregistrement des routes pour les propriétés via un blueprint
app.register_blueprint(property_blueprint)


# Route pour vérifier si l'application fonctionne correctement
@app.route('/',methods=['GET'])
def health_check():
    return {"status":"healthy"},200

