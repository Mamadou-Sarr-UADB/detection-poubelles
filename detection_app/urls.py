from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resultat/<int:detection_id>/', views.resultat, name='resultat'),
    path('historique/', views.historique, name='historique'),
    path('statistiques/', views.statistiques, name='statistiques'),
]
