"""
Ce module définit les modèles de données et initialise les extensions nécessaires 
pour la gestion des utilisateurs.

Contenu:
- Initialisation de SQLAlchemy (pour la gestion de la base de données).
- Initialisation de Flask-Bcrypt (pour le hachage des mots de passe).
- Définition du modèle `Utilisateur`, qui représente un utilisateur dans la base de données.
"""


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# Initialisation de l'instance SQLAlchemy
# Permet la gestion des interactions avec la base de données.
db = SQLAlchemy()

# Initialisation de Flask-Bcrypt
# Utilisé pour sécuriser les mots de passe en les hachant.
bcrypt =Bcrypt()

class Utilisateur(db.Model):
    """Modèle représentant un utilisateur.

    Attributs:
        - id (int): Identifiant unique de l'utilisateur.
        - email (str): Adresse email unique de l'utilisateur.
        - password_hash (str): Hachage sécurisé du mot de passe.
        - nom (str): Nom de l'utilisateur.
        - prenom (str): Prénom de l'utilisateur.
        - date_de_naissance (date): Date de naissance de l'utilisateur.

    Méthodes:
        - set_password(password): Hache le mot de passe avant de le sauvegarder.
        - check_password(password): Vérifie si un mot de passe correspond au hachage.
    
    """
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    nom = db.Column(db.String(50),nullable=False)
    prenom = db.Column(db.String(50),nullable=False)
    date_de_naissance = db.Column(db.Date,nullable=False)

    def set_password(self,password):
        """Hache un mot de passe fourni et le stocke dans l'attribut `password_hash`.

        Paramètres:
            - password (str): Mot de passe en clair à hacher.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Vérifie si un mot de passe correspond au hachage stocké.

        Paramètres:
            - password (str): Mot de passe en clair à vérifier.

        Retourne:
            - bool: True si le mot de passe est correct, False sinon.
        """
        return bcrypt.check_password_hash(self.password_hash,password)
