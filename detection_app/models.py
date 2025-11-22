from django.db import models

class ImageDetection(models.Model):
    """Modèle pour stocker les images uploadées et les résultats"""
    image = models.ImageField(upload_to='uploads/')
    image_resultat = models.ImageField(upload_to='resultats/', blank=True, null=True)
    date_upload = models.DateTimeField(auto_now_add=True)
    
    # Résultats de détection
    nombre_poubelles = models.IntegerField(default=0)
    nombre_vides = models.IntegerField(default=0)
    nombre_pleines = models.IntegerField(default=0)
    
    # Détails JSON
    detections_json = models.JSONField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_upload']
    
    def __str__(self):
        return f"Detection {self.id} - {self.date_upload.strftime('%Y-%m-%d %H:%M')}"
