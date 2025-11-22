import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import os
from django.conf import settings

# Charger le modèle YOLO une seule fois au démarrage
MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'yolo_poubelles.pt')
modele = YOLO(MODEL_PATH)

def detecter_poubelles(chemin_image, detection_id):
    """
    Détecte et classifie les poubelles dans une image
    
    Args:
        chemin_image: Chemin vers l'image uploadée
        detection_id: ID de la détection pour nommer l'image résultat
    
    Returns:
        dict avec les résultats
    """
    # Charger l'image
    image = cv2.imread(chemin_image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Prédiction avec YOLO
    resultats = modele(image, conf=0.5, verbose=False)
    
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
            nom_classe = modele.names[classe_id]
            
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
