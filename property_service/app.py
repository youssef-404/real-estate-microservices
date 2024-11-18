from flask import Flask
from google.cloud import datastore
from dotenv import load_dotenv
from property_service.routes import property_blueprint
from flask_jwt_extended import JWTManager
import os

load_dotenv()

app = Flask(__name__)

credentials_path =os.getenv("DATASTORE_CREDENTIALS")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")

jwt = JWTManager(app)


if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS n'est pas défini dans le fichier .env.")

app.config['DATASTORE_CLIENT'] = datastore.Client.from_service_account_json(credentials_path)

app.register_blueprint(property_blueprint)

@app.route('/',methods=['GET'])
def health_check():
    return {"status":"healthy"},200

