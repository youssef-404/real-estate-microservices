# **Gestion Immobilière - Microservices**

## **Description du Projet**

Ce projet est une application de gestion immobilière construite en utilisant une architecture basée sur des **microservices**. Il permet aux utilisateurs de :
- Créer et gérer des propriétés immobilières (nom, description, type de bien, ville, pièces, propriétaire, etc.).
- Modifier leurs informations personnelles (nom, prénom, date de naissance).
- Consulter les propriétés disponibles dans une ville spécifique.
- Mettre à jour ou supprimer une propriété (uniquement pour le propriétaire).

---

## **Architecture**

L'application est divisée en deux principaux microservices :

### **1. Service Utilisateur (`user_service`)**
Ce service gère tout ce qui concerne les utilisateurs, notamment :
- Enregistrement des utilisateurs.
- Authentification via JWT.
- Mise à jour et suppression des informations des utilisateurs.
- Validation des utilisateurs pour d'autres services.


### **2. Service Propriété (`property_service`)**
Ce service gère les propriétés immobilières, notamment :
- Création, mise à jour et suppression des propriétés.
- Filtrage des propriétés par ville.
- Validation du propriétaire via le service utilisateur.

### **Technologies Utilisées**
| Composant           | Technologie              |
|----------------------|--------------------------|
| **Framework**        | Flask                   |
| **Base de données**  | SQLite/MySQL (service utilisateur), Google Cloud Datastore (service propriété) |
| **Auth**             | Flask-JWT-Extended      |
| **Hashing MDP**      | Flask-Bcrypt            |
| **Communication**    | RESTful APIs avec `requests` |

---

## **Modèle de Données**

### **1. Modèle Utilisateur (dans `user_service`)**
| Champ             | Type         | Description                            |
|--------------------|--------------|----------------------------------------|
| `id`              | Integer      | Identifiant unique de l'utilisateur.  |
| `email`           | String       | Adresse email unique.                 |
| `password_hash`   | String       | Hash du mot de passe.                 |
| `nom`             | String       | Nom de l'utilisateur.                 |
| `prenom`          | String       | Prénom de l'utilisateur.              |
| `date_de_naissance` | Date       | Date de naissance de l'utilisateur.   |

### **2. Modèle Propriété (dans `property_service`)**
| Champ             | Type         | Description                            |
|--------------------|--------------|----------------------------------------|
| `nom`             | String       | Nom de la propriété.                  |
| `description`     | String       | Description de la propriété.          |
| `type_de_bien`    | String       | Type de bien (Maison, Appartement, etc.). |
| `ville`           | String       | Ville où se trouve la propriété.      |
| `proprietaire`    | Integer      | Identifiant du propriétaire (référence au service utilisateur). |
| `pieces`          | Liste        | Liste des caractéristiques des pièces. |


---

## **Configuration des Fichiers `.env`**

Chaque microservice utilise un fichier `.env` pour stocker les variables d'environnement nécessaires à son fonctionnement. 

### **1. Service Utilisateur**

Le fichier `.env` doit être créé dans le dossier `user_service` :

```ini
# URI de la base de données (MySQL ou SQLite)
SQLALCHEMY_DATABASE_URI=mysql://<user>:<password>@<host>/<database>

# Clé secrète JWT pour l'authentification
JWT_SECRET_KEY=jwt_secret_key

PORT = 5000
```

**Remarque :**
- Si vous souhaitez utiliser **MySQL**, remplacez `<user>`, `<password>`, `<host>` et `<database>` par les informations de connexion à votre base MySQL.
- Si aucun `SQLALCHEMY_DATABASE_URI` n'est défini, l'application utilisera par défaut SQLite avec un fichier `utilisateurs.db`.

---

### **2. Service Propriété**

Le fichier `.env` doit être créé dans le dossier `property_service` :

```ini
# Chemin vers le fichier de configuration Google Cloud Datastore
DATASTORE_CREDENTIALS=datastoreconfig.json

# URL du service utilisateur pour la validation des propriétaires
USER_SERVICE_URL=http://localhost:5000

PORT=5001
```

**Remarque :**
- Le fichier `datastoreconfig.json` doit être généré depuis Google Cloud Console. Pour cela :
  1. Allez dans votre projet Google Cloud.
  2. Accédez à la section **API et Services > Identifiants**.
  3. Créez une **clé JSON** pour votre compte de service Datastore et téléchargez-la.
  4. Placez ce fichier dans le dossier `property_service` et définissez son chemin dans `DATASTORE_CREDENTIALS`.


## **Installation et Configuration**

### **Prérequis**
- Python 3.8+

### **Étapes d'Installation**

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/youssef-404/real-estate-microservices.git
   cd real-estate-microservices
   ```

2. **Configurer les environnements virtuels :**
   - Pour `user_service` :
     ```bash
     python -m venv user_service\venv
     user_service\venv\Scripts\activate # Sur linux : source user_service/venv/bin/activate
     pip install -r user_service\requirements.txt
     ```
   - Pour `property_service` :
     ```bash
     python -m venv property_service\venv
     property_service\venv\Scripts\activate # Sur linux : source property_service/venv/bin/activate
     pip install -r property_service\requirements.txt
     ```

3. **Configurer les fichiers `.env` :**
   - Suivez les instructions pour chaque service décrites plus haut.

---

## **Lancer l'Application**

1. **Lancer le service utilisateur :**
   ```bash
   python -m user_service.run
   ```

2. **Lancer le service propriété :**
   ```bash
   python -m property_service.run
   ```

3. **Tester les endpoints :**
   - Service utilisateur : `http://localhost:5000`
   - Service propriété : `http://localhost:5001`

---

## **Utilisation de l'API**

### **1. Endpoints du Service Utilisateur**

| Méthode | Endpoint                | Description                                |
|---------|-------------------------|--------------------------------------------|
| `POST`  | `/users`                | Enregistrer un nouvel utilisateur.         |
| `POST`  | `/login`                | Authentifier un utilisateur.               |
| `GET`   | `/users/<id>`           | Récupérer les informations d'un utilisateur. |
| `PUT`   | `/users/<id>`           | Mettre à jour les informations d'un utilisateur. |
| `DELETE`| `/users/<id>`           | Supprimer un utilisateur.                  |

### **2. Endpoints du Service Propriété**

| Méthode | Endpoint                 | Description                                |
|---------|--------------------------|--------------------------------------------|
| `POST`  | `/properties`            | Ajouter une nouvelle propriété.            |
| `GET`   | `/properties?city=<Ville>`  | Lister les propriétés par ville.           |
| `GET`   | `/properties/<id>`       | Récupérer une propriété par son ID.        |
| `PUT`   | `/properties/<id>`       | Mettre à jour une propriété existante.     |
| `DELETE`| `/properties/<id>`       | Supprimer une propriété existante.         |

---





