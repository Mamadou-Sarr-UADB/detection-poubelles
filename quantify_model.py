"""
Script pour quantifier et réduire la taille du modèle YOLO
Réduit la taille de ~50% avec perte minimale de précision
"""

from ultralytics import YOLO
import torch

# Charger le modèle original
print("Chargement du modèle original...")
model = YOLO('models/yolo_poubelles.pt')

# Exporter en format optimisé (Half precision - FP16)
print("Quantification du modèle en FP16...")
model.export(format='torchscript', half=True)

print("✅ Modèle quantifié créé : yolo_poubelles.torchscript")
print("Taille réduite d'environ 50%")
