# 🗑️ Détection de Poubelles avec YOLOv8 + Django

Application web Django pour détecter et classifier les poubelles (pleines/vides) à partir d'images uploadées par les utilisateurs.

## 🚀 Installation Rapide

1. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

2. **Lancer l'application :**
```bash
python manage.py runserver
```
Ou double-cliquez sur `lancer_django.bat`

3. **Accéder à l'application :**
Ouvrez http://localhost:8000 dans votre navigateur

## 📂 Structure du Projet

```
├── detection_projet/          # Configuration Django
├── detection_app/             # Application principale
│   ├── models.py             # Modèle BDD (ImageDetection)
│   ├── views.py              # Vues (home, resultat, historique)
│   ├── utils.py              # Détection YOLO
│   ├── templates/            # Templates HTML
│   └── migrations/           # Migrations BDD
├── models/
│   └── yolo_poubelles.pt     # Modèle YOLO entraîné ⭐
├── media/                     # Images uploadées et résultats
├── My-First-Project-2/        # Dataset Roboflow
├── detection_poubelles.ipynb  # Notebook d'entraînement
├── manage.py                  # Gestionnaire Django
└── db.sqlite3                 # Base de données
```

## ✨ Fonctionnalités

✅ **Upload d'images** - Interface intuitive  
✅ **Détection automatique** - Modèle YOLOv8 entraîné  
✅ **Classification** - Poubelles pleines vs vides  
✅ **Visualisation** - Image avant/après avec annotations  
✅ **Statistiques** - Nombre détecté, vides, pleines  
✅ **Historique** - Conservation de toutes les détections  
✅ **Interface moderne** - Design responsive et attractif

## 🎯 Utilisation

1. Accédez à http://localhost:8000
2. Cliquez sur la zone d'upload
3. Sélectionnez une image de poubelle
4. Visualisez instantanément les résultats !

## 📊 Pages Disponibles

- **Accueil** (`/`) - Upload et détections récentes
- **Résultat** (`/resultat/<id>/`) - Détails d'une détection
- **Historique** (`/historique/`) - Toutes les détections

## 🛠️ Modèle YOLO

- **Type :** YOLOv8 Nano (rapide et léger)
- **Classes :** 
  - `poubelle_vide` (0)
  - `poubelle_pleine` (1)
- **Source :** Entraîné sur Roboflow (370 images)
- **Localisation :** `models/yolo_poubelles.pt`

## 📓 Notebook Jupyter

Le fichier `detection_poubelles.ipynb` contient :
- Téléchargement du dataset depuis Roboflow
- Configuration et entraînement YOLO
- Fonctions de détection et validation
- Toutes les fonctions en français

## 🔧 Administration

Pour accéder à l'interface admin Django :

```bash
python manage.py createsuperuser
```

Puis : http://localhost:8000/admin

## 📝 Technologies

- **Backend :** Django 5.2
- **Deep Learning :** YOLOv8 (Ultralytics)
- **Vision :** OpenCV
- **Base de données :** SQLite
- **Frontend :** HTML/CSS (templates Django)

## 🎓 Projet Deep Learning

Système de détection et classification de poubelles utilisant l'apprentissage profond avec YOLO pour améliorer la gestion des déchets.

---

**© 2025 - Projet de Deep Learning avec YOLOv8**
