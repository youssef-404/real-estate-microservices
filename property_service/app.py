from flask import Flask
from google.cloud import datastore
from dotenv import load_dotenv
from property_service.routes import property_blueprint
import os

load_dotenv()

app = Flask(__name__)

credentials_path =os.getenv("DATASTORE_CREDENTIALS")


if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS n'est pas défini dans le fichier .env.")

app.config['DATASTORE_CLIENT'] = datastore.Client.from_service_account_json(credentials_path)

app.register_blueprint(property_blueprint)

@app.route('/',methods=['GET'])
def health_check():
    return {"status":"healthy"},200

