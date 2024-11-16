from flask import Flask
from models import db, bcrypt
from routes import utilisateur_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utilisateurs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()


    
@app.route('/',methods=['GET'])
def health_check():
    return {"status":"healthy"},200


app.register_blueprint(utilisateur_blueprint)

if __name__ == '__main__':
    app.run(debug=True)