# Instructions pour déployer le modèle YOLO

Le fichier `models/yolo_poubelles.pt` est trop volumineux pour GitHub (limite 100MB).

## Solution : Google Drive

### 1. Uploader le modèle sur Google Drive

1. Allez sur https://drive.google.com
2. Uploadez le fichier `models/yolo_poubelles.pt`
3. Faites un clic droit → "Partager" → "Obtenir le lien"
4. Changez en "Tous les utilisateurs ayant le lien"
5. Copiez l'ID du fichier (la partie après `/d/` dans l'URL)

Exemple d'URL : `https://drive.google.com/file/d/1ABC123xyz/view`
L'ID est : `1ABC123xyz`

### 2. Ajouter la variable d'environnement sur Render

Dans Render → Settings → Environment Variables :
- Key : `YOLO_MODEL_URL`
- Value : `https://drive.google.com/uc?export=download&id=VOTRE_ID_ICI`

### 3. Le modèle sera téléchargé automatiquement au premier démarrage

Le code dans `utils.py` téléchargera le modèle si nécessaire.
