from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt =Bcrypt()

class Utilisateur(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    nom = db.Column(db.String(50),nullable=False)
    prenom = db.Column(db.String(50),nullable=False)
    date_de_naissance = db.Column(db.Date,nullable=False)

    def set_password(self,password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash,password)
