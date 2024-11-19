"""
Application principale pour le service utilisateur.

Ce fichier configure l'application Flask, initialise les extensions nécessaires et enregistre les routes pour les utilisateurs.

Points principaux :
- Chargement de la configuration.
- Initialisation de la base de données.
- Enregistrement des blueprints.
"""


from flask import Flask
from flask_jwt_extended import JWTManager
from user_service.models import db, bcrypt
from user_service.routes import user_blueprint
from user_service.config import Config

# Création de l'application Flask
app = Flask(__name__)

# Chargement de la configuration
app.config.from_object(Config)

# Initialisation des extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Enregistrement des routes 
app.register_blueprint(user_blueprint)

# Création des tables dans la base de données si elles n'existent pas
with app.app_context():
    db.create_all()


# Route pour vérifier l'état de l'application
@app.route('/',methods=['GET'])
def health_check():
    return {"status":"healthy"},200
