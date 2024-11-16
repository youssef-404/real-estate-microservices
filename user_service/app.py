from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from routes import utilisateur_blueprint
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utilisateurs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(utilisateur_blueprint)


with app.app_context():
    db.create_all()


    
@app.route('/',methods=['GET'])
def health_check():
    return {"status":"healthy"},200



if __name__ == '__main__':
    app.run(debug=True)