"""
Script de conversion YOLO vers ONNX
Réduit la taille et améliore les performances
"""

from ultralytics import YOLO
import os

print("=" * 50)
print("Conversion YOLO → ONNX")
print("=" * 50)

# Charger le modèle YOLO
model_path = 'models/yolo_poubelles.pt'
print(f"\n1. Chargement du modèle: {model_path}")
model = YOLO(model_path)

# Exporter en ONNX
print("\n2. Conversion en ONNX...")
print("   - Format: ONNX")
print("   - Optimisé pour CPU")
print("   - Réduction de taille attendue: ~50%")

onnx_path = model.export(
    format='onnx',
    simplify=True,  # Simplifie le graphe ONNX
    opset=12,       # Version ONNX compatible
    dynamic=False   # Taille fixe pour performance
)

print(f"\n3. ✅ Conversion terminée!")
print(f"   Fichier créé: {onnx_path}")

# Vérifier la taille
import os
original_size = os.path.getsize(model_path) / (1024 * 1024)
onnx_size = os.path.getsize(onnx_path) / (1024 * 1024)
reduction = ((original_size - onnx_size) / original_size) * 100

print(f"\n4. Comparaison des tailles:")
print(f"   Original (.pt):  {original_size:.2f} MB")
print(f"   ONNX (.onnx):    {onnx_size:.2f} MB")
print(f"   Réduction:       {reduction:.1f}%")

print("\n5. Prochaine étape:")
print("   → Le modèle ONNX sera utilisé automatiquement")
print("=" * 50)
