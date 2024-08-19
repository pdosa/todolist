Voici une documentation complète pour votre application FastAPI, qui inclut l'inscription, la connexion et la gestion des tâches.

---

# Documentation de l'Application FastAPI

## Introduction

Cette application FastAPI permet aux utilisateurs de s'inscrire, de se connecter et de gérer leurs tâches (todos). Elle utilise JSON pour stocker les données des utilisateurs et des tâches, ainsi que JWT pour l'authentification.

### Fonctionnalités Principales

- Inscription d'utilisateurs avec un hachage de mot de passe sécurisé.
- Connexion via OAuth2 avec JWT pour l'authentification.
- Gestion des tâches pour les utilisateurs connectés (ajout de nouvelles tâches).
- Persistance des données des utilisateurs et des tâches dans un fichier JSON.

## Technologies Utilisées

- **Backend :** FastAPI
- **Base de données :** Fichier JSON (`db.json`)
- **Sécurité :** OAuth2 avec JWT
- **Gestion des mots de passe :** Hachage avec `passlib`
- **Frontend :** HTML, CSS, et JS servis par FastAPI
- **Serveur de fichiers statiques :** `StaticFiles` de FastAPI

---

## Configuration de l'Environnement

### Pré-requis

- Python 3.8 ou supérieur
- PIP (Python Package Manager)

### Installation des Dépendances

1. Clonez ou téléchargez ce projet.
2. Naviguez dans le répertoire du projet et installez les dépendances avec la commande suivante :

```bash
pip install fastapi[all] passlib[bcrypt] python-jose
```

### Structure du Projet

```bash
.
├── main.py                     # Fichier principal de l'application FastAPI
├── db.json                     # Fichier JSON simulant la base de données
├── vues/                       # Dossier contenant les fichiers HTML
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
├── static/                     # Dossier contenant les fichiers statiques (CSS, JS, images)
└── README.md                   # Documentation du projet
```

---

## API Endpoints

### 1. Inscription d'un Utilisateur

- **URL :** `/register`
- **Méthode :** `POST`
- **Description :** Inscrit un nouvel utilisateur dans l'application.
- **Requête :**
  - **Corps de la requête (JSON)** :
    ```json
    {
      "name": "Nom de l'utilisateur",
      "email": "email@example.com",
      "password": "password123"
    }
    ```
- **Réponse :**
  - **Réponse réussie (200 OK)** :
    ```json
    {
      "id": 1,
      "name": "Nom de l'utilisateur",
      "email": "email@example.com",
      "hashed_password": "$2b$12$hashedpasswordstring",
      "todos": []
    }
    ```
  - **Erreurs possibles :**
    - **400 Bad Request :** Email déjà enregistré

### 2. Connexion (Obtenir un Jeton JWT)

- **URL :** `/token`
- **Méthode :** `POST`
- **Description :** Authentifie l'utilisateur et retourne un jeton JWT.
- **Requête :**
  - **Corps de la requête (Formulaire)** :
    - `username`: Email de l'utilisateur
    - `password`: Mot de passe de l'utilisateur
- **Réponse :**
  - **Réponse réussie (200 OK)** :
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```
  - **Erreurs possibles :**
    - **400 Bad Request :** Email ou mot de passe incorrect

### 3. Ajouter une Tâche

- **URL :** `/todos`
- **Méthode :** `POST`
- **Description :** Ajoute une nouvelle tâche pour l'utilisateur connecté.
- **Authentification :** Requiert un jeton JWT (OAuth2).
- **Requête :**
  - **Paramètres de la requête (Formulaire)** :
    - `title`: Titre de la tâche
    - `description`: Description de la tâche
- **Réponse :**
  - **Réponse réussie (200 OK)** :
    ```json
    {
      "msg": "Todo added",
      "todo": {
        "id": 1,
        "title": "Ma Tâche",
        "description": "Détails de la tâche",
        "start": "2024-08-19",
        "end": "2024-08-24",
        "priority": "high"
      }
    }
    ```
  - **Erreurs possibles :**
    - **401 Unauthorized :** Jeton JWT invalide ou expiré

---

## Gestion des Fichiers Statique et HTML

### Fichiers HTML

L'application sert trois fichiers HTML principaux :

1. **Page d'inscription :** `/register`
2. **Page de connexion :** `/login`
3. **Tableau de bord (ajout de tâches) :** `/dashboard`

Ces fichiers sont situés dans le dossier `vues/` et peuvent être accédés via les routes appropriées dans FastAPI.

### Fichiers CSS et JS

Les fichiers statiques (CSS, JS) doivent être placés dans le dossier `static/`. Vous pouvez référencer ces fichiers dans vos fichiers HTML en utilisant des chemins relatifs comme suit :

```html
<link rel="stylesheet" href="/static/style.css">
<script src="/static/app.js"></script>
```

---

## Authentification et Sécurité

### Gestion des Mots de Passe

Les mots de passe des utilisateurs sont sécurisés à l'aide de l'algorithme de hachage bcrypt via la bibliothèque `passlib`.

### JWT (JSON Web Tokens)

L'application utilise JWT pour l'authentification des utilisateurs. Les jetons sont générés lors de la connexion et doivent être envoyés avec chaque requête authentifiée (comme l'ajout de tâches).

**Utilisation du Jeton JWT :**

- Après une connexion réussie, le jeton JWT doit être inclus dans l'en-tête `Authorization` sous la forme `Bearer <token>` pour les requêtes nécessitant une authentification.

### Durée du Jeton

Les jetons JWT expirent après 30 minutes, mais cette durée peut être modifiée en ajustant la variable `ACCESS_TOKEN_EXPIRE_MINUTES`.

---

## Gestion de la Base de Données

### Fichier JSON (`db.json`)

Les utilisateurs et les tâches sont stockés dans un fichier JSON nommé `db.json`. Ce fichier agit comme une base de données pour cette application simple.

- Lorsqu'un nouvel utilisateur s'inscrit, ses informations (y compris son mot de passe haché) sont ajoutées au fichier.
- Lorsque l'utilisateur ajoute des tâches, celles-ci sont également ajoutées au fichier JSON sous l'utilisateur correspondant.

### Format de la Base de Données

Voici un exemple de contenu du fichier `db.json` :

```json
[
    {
        "id": 1,
        "name": "Nom de l'utilisateur",
        "email": "email@example.com",
        "hashed_password": "$2b$12$hashedpasswordstring",
        "todos": [
            {
                "id": 1,
                "title": "Ma Tâche",
                "description": "Détails de la tâche",
                "start": "2024-08-19",
                "end": "2024-08-24",
                "priority": "high"
            }
        ]
    }
]
```

---

## Déploiement

### Lancer l'application en local

Pour lancer l'application en local, exécutez la commande suivante dans le terminal :

```bash
uvicorn main:app --reload
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000`.

### Déploiement sur un Serveur

Pour déployer cette application sur un serveur, vous pouvez utiliser un gestionnaire de processus comme **Gunicorn** avec Uvicorn en tant que worker. Par exemple :

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

---

## Conclusion

Cette application FastAPI est une solution simple pour gérer l'inscription des utilisateurs, la connexion, et la gestion des tâches avec un fichier JSON en tant que base de données. Elle est extensible et peut être intégrée à une base de données plus robuste (comme PostgreSQL ou MySQL) si nécessaire.