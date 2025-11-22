from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from .models import ImageDetection
from .utils import detecter_poubelles
import os
import json

def home(request):
    """Page d'accueil avec upload d'image"""
    if request.method == 'POST' and request.FILES.get('image'):
        # Sauvegarder l'image uploadée
        image_file = request.FILES['image']
        detection = ImageDetection.objects.create(image=image_file)
        
        # Effectuer la détection
        chemin_image = detection.image.path
        resultats = detecter_poubelles(chemin_image, detection.id)
        
        # Mettre à jour les résultats
        detection.nombre_poubelles = resultats['total']
        detection.nombre_vides = resultats['vides']
        detection.nombre_pleines = resultats['pleines']
        detection.detections_json = resultats['detections']
        detection.image_resultat = resultats['chemin_resultat']
        detection.save()
        
        return redirect('resultat', detection_id=detection.id)
    
    # Afficher les dernières détections
    detections_recentes = ImageDetection.objects.all()[:10]
    
    return render(request, 'detection_app/home.html', {
        'detections_recentes': detections_recentes
    })

def resultat(request, detection_id):
    """Afficher les résultats d'une détection"""
    detection = get_object_or_404(ImageDetection, id=detection_id)
    
    return render(request, 'detection_app/resultat.html', {
        'detection': detection
    })

def historique(request):
    """Afficher l'historique de toutes les détections"""
    detections = ImageDetection.objects.all()
    
    return render(request, 'detection_app/historique.html', {
        'detections': detections
    })

def statistiques(request):
    """Page de statistiques avec graphiques"""
    # Statistiques globales
    total_detections = ImageDetection.objects.count()
    total_poubelles = ImageDetection.objects.aggregate(Sum('nombre_poubelles'))['nombre_poubelles__sum'] or 0
    total_vides = ImageDetection.objects.aggregate(Sum('nombre_vides'))['nombre_vides__sum'] or 0
    total_pleines = ImageDetection.objects.aggregate(Sum('nombre_pleines'))['nombre_pleines__sum'] or 0
    
    # Détections par jour (derniers 7 jours)
    detections_par_jour = ImageDetection.objects.annotate(
        date=TruncDate('date_upload')
    ).values('date').annotate(
        total=Count('id'),
        vides=Sum('nombre_vides'),
        pleines=Sum('nombre_pleines')
    ).order_by('date')[:7]
    
    # Préparer les données pour Chart.js
    dates = [d['date'].strftime('%d/%m') for d in detections_par_jour]
    totaux = [d['total'] for d in detections_par_jour]
    vides_par_jour = [d['vides'] or 0 for d in detections_par_jour]
    pleines_par_jour = [d['pleines'] or 0 for d in detections_par_jour]
    
    context = {
        'total_detections': total_detections,
        'total_poubelles': total_poubelles,
        'total_vides': total_vides,
        'total_pleines': total_pleines,
        'dates_json': json.dumps(dates),
        'totaux_json': json.dumps(totaux),
        'vides_json': json.dumps(vides_par_jour),
        'pleines_json': json.dumps(pleines_par_jour),
    }
    
    return render(request, 'detection_app/statistiques.html', context)
