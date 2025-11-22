# Guide de Déploiement - Détection de Poubelles

## 📦 Préparation pour le déploiement

### 1. Fichiers créés pour vous :
- ✅ `.gitignore` - Exclut les fichiers sensibles
- ✅ `Procfile` - Configuration Heroku/Railway
- ✅ `runtime.txt` - Version Python
- ✅ `.env.example` - Template pour variables d'environnement
- ✅ `requirements.txt` - Dépendances mises à jour

## 🚀 Déploiement sur différentes plateformes

### Option 1: GitHub + Heroku (Recommandé)

#### Étape 1: Préparer le projet

1. **Mettre à jour settings.py pour la production**

Ajoutez en haut de `detection_projet/settings.py` :

```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-not-for-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
```

Ajoutez dans MIDDLEWARE (après SecurityMiddleware) :

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajouter cette ligne
    # ... reste du middleware
]
```

Ajoutez à la fin du fichier :

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### Étape 2: Initialiser Git et pousser sur GitHub

```bash
# Initialiser le repository
git init
git add .
git commit -m "Initial commit - Detection Poubelles App"

# Créer un repository sur GitHub (allez sur github.com/new)
# Puis connecter votre projet :
git remote add origin https://github.com/VOTRE_USERNAME/detection-poubelles.git
git branch -M main
git push -u origin main
```

#### Étape 3: Déployer sur Heroku

```bash
# Installer Heroku CLI : https://devcenter.heroku.com/articles/heroku-cli

# Se connecter
heroku login

# Créer l'application
heroku create nom-de-votre-app

# Configurer les variables d'environnement
heroku config:set SECRET_KEY="votre-secret-key-generee"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=nom-de-votre-app.herokuapp.com

# Déployer
git push heroku main

# Effectuer les migrations
heroku run python manage.py migrate

# Ouvrir l'application
heroku open
```

**⚠️ Important pour Heroku :**
- Le modèle YOLO (`models/yolo_poubelles.pt`) est trop volumineux
- Solution : Uploadez-le sur Google Drive ou un service de stockage
- Modifiez `utils.py` pour télécharger le modèle au démarrage

### Option 2: Railway (Plus simple)

1. **Allez sur [Railway.app](https://railway.app)**
2. Connectez votre compte GitHub
3. Cliquez sur "New Project" → "Deploy from GitHub repo"
4. Sélectionnez votre repository
5. Railway détecte automatiquement Django
6. Ajoutez les variables d'environnement dans Settings :
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=votre-domaine.railway.app`
7. Déployez !

### Option 3: Render

1. **Allez sur [Render.com](https://render.com)**
2. Créez un nouveau "Web Service"
3. Connectez votre repository GitHub
4. Configuration :
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn detection_projet.wsgi:application`
5. Ajoutez les variables d'environnement
6. Déployez !

### Option 4: PythonAnywhere (Gratuit)

1. **Allez sur [PythonAnywhere.com](https://www.pythonanywhere.com)**
2. Créez un compte gratuit
3. Ouvrez un terminal Bash
4. Clonez votre repository :
```bash
git clone https://github.com/VOTRE_USERNAME/detection-poubelles.git
cd detection-poubelles
```
5. Créez un environnement virtuel :
```bash
mkvirtualenv --python=/usr/bin/python3.10 detection-env
pip install -r requirements.txt
```
6. Configurez l'application web dans l'onglet "Web"
7. Éditez le fichier WSGI pour pointer vers votre projet
8. Rechargez l'application

## 📝 Checklist avant déploiement

- [ ] `.gitignore` créé et configuré
- [ ] `requirements.txt` avec versions spécifiques
- [ ] `Procfile` pour Heroku/Railway
- [ ] `runtime.txt` avec version Python
- [ ] Variables d'environnement configurées
- [ ] `DEBUG=False` en production
- [ ] `ALLOWED_HOSTS` configuré
- [ ] WhiteNoise installé pour les fichiers statiques
- [ ] Migrations créées et testées
- [ ] Modèle YOLO accessible (Drive/S3/URL)

## 🔐 Sécurité

**IMPORTANT :** Ne commitez JAMAIS :
- Votre `SECRET_KEY` Django
- Le fichier `db.sqlite3` avec données sensibles
- Les fichiers `.env`
- Les modèles volumineux (>100MB)

## 📊 Hébergement du modèle YOLO

Le fichier `yolo_poubelles.pt` est trop gros pour GitHub/Heroku.

**Solutions :**

1. **Google Drive** (Recommandé)
```python
# Dans utils.py
import gdown

MODEL_URL = 'https://drive.google.com/uc?id=VOTRE_FILE_ID'
MODEL_PATH = 'models/yolo_poubelles.pt'

if not os.path.exists(MODEL_PATH):
    os.makedirs('models', exist_ok=True)
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
```

2. **AWS S3 / Azure Blob Storage**
3. **Git LFS** (Git Large File Storage)

## 🆘 Problèmes courants

### "Application error" sur Heroku
- Vérifiez les logs : `heroku logs --tail`
- Assurez-vous que gunicorn est installé
- Vérifiez que `ALLOWED_HOSTS` contient votre domaine

### "Module not found"
- Vérifiez `requirements.txt`
- Relancez : `pip install -r requirements.txt`

### Fichiers statiques ne se chargent pas
- Exécutez : `python manage.py collectstatic`
- Vérifiez que WhiteNoise est configuré

### Le modèle ne se charge pas
- Vérifiez que le fichier existe
- Vérifiez les permissions
- Utilisez une solution de stockage externe

## 🎉 C'est prêt !

Une fois déployé, votre application sera accessible publiquement !

Partagez le lien : `https://votre-app.herokuapp.com` 🚀
