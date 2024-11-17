from flask import Flask
from flask_jwt_extended import JWTManager
from user_service.models import db, bcrypt
from user_service.routes import utilisateur_blueprint
from user_service.config import Config, TestConfig
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

if app.config['TESTING']:
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(utilisateur_blueprint)


with app.app_context():
    db.create_all()


    
@app.route('/',methods=['GET'])
def health_check():
    return {"status":"healthy"},200
