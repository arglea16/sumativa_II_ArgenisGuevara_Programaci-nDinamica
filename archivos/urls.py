from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('registro/', views.registro, name='registro'),
    path('descargar/<int:pk>/', views.descargar, name='descargar'),
    path('compartir/<int:pk>/', views.compartir, name='compartir'),
    path('eliminar/<int:pk>/', views.eliminar, name='eliminar'),
    path('c/<uuid:token>/', views.publico, name='publico'),
]