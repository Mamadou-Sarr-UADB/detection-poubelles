import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import os
import requests
from django.conf import settings

# Variable globale pour le modèle
modele = None

def telecharger_modele_depuis_drive(file_id, destination):
    """Télécharge le modèle depuis Google Drive"""
    print(f"Téléchargement du modèle YOLO depuis Google Drive...")
    
    # URL de téléchargement direct Google Drive
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    session = requests.Session()
    response = session.get(URL, stream=True)
    
    # Gérer la confirmation de téléchargement pour les gros fichiers
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': file_id, 'confirm': value}
            response = session.get(URL, params=params, stream=True)
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Télécharger le fichier
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)
    
    print(f"Modèle téléchargé avec succès: {destination}")

def charger_modele():
    """Charge le modèle YOLO si ce n'est pas déjà fait"""
    global modele
    if modele is None:
        MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'yolo_poubelles.pt')
        
        # Si le modèle n'existe pas, le télécharger depuis Google Drive
        if not os.path.exists(MODEL_PATH):
            DRIVE_FILE_ID = "12XxkEpl74l-YgTTwjzninJ2wkt3PsTBk"
            telecharger_modele_depuis_drive(DRIVE_FILE_ID, MODEL_PATH)
        
        modele = YOLO(MODEL_PATH)
        print(f"Modèle YOLO chargé: {modele.names}")
    return modele

def detecter_poubelles(chemin_image, detection_id):
    """
    Détecte et classifie les poubelles dans une image
    
    Args:
        chemin_image: Chemin vers l'image uploadée
        detection_id: ID de la détection pour nommer l'image résultat
    
    Returns:
        dict avec les résultats
    """
    # Charger le modèle
    model = charger_modele()
    
    # Charger l'image
    image = cv2.imread(chemin_image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Prédiction avec YOLO
    resultats = model(image, conf=0.5, verbose=False)
    
    detections = []
    nb_vides = 0
    nb_pleines = 0
    
    for resultat in resultats:
        boxes = resultat.boxes
        
        for box in boxes:
            # Extraire les informations
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            confiance = float(box.conf[0].cpu().numpy())
            classe_id = int(box.cls[0].cpu().numpy())
            nom_classe = model.names[classe_id]
            
            # Déterminer l'état
            etat = 'vide' if 'vide' in nom_classe.lower() or 'empty' in nom_classe.lower() else 'plein'
            
            if etat == 'vide':
                nb_vides += 1
            else:
                nb_pleines += 1
            
            # Stocker la détection
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confiance': round(confiance * 100, 1),  # Convertir en pourcentage
                'classe': nom_classe,
                'etat': etat
            })
            
            # Dessiner sur l'image
            couleur = (0, 255, 0) if etat == 'vide' else (255, 0, 0)
            cv2.rectangle(image_rgb, (x1, y1), (x2, y2), couleur, 3)
            
            # Texte
            texte = f"{etat.upper()} ({confiance*100:.0f}%)"
            
            # Fond pour le texte
            (text_width, text_height), _ = cv2.getTextSize(
                texte, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2
            )
            cv2.rectangle(
                image_rgb, 
                (x1, y1 - text_height - 10), 
                (x1 + text_width, y1), 
                couleur, 
                -1
            )
            
            cv2.putText(
                image_rgb, texte, (x1, y1-5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2
            )
    
    # Sauvegarder l'image avec les détections
    resultats_dir = os.path.join(settings.MEDIA_ROOT, 'resultats')
    os.makedirs(resultats_dir, exist_ok=True)
    
    nom_fichier = f"resultat_{detection_id}.jpg"
    chemin_resultat = os.path.join(resultats_dir, nom_fichier)
    
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(chemin_resultat, image_bgr)
    
    return {
        'total': len(detections),
        'vides': nb_vides,
        'pleines': nb_pleines,
        'detections': detections,
        'chemin_resultat': f'resultats/{nom_fichier}'
    }
