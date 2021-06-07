from django.urls import path
from . import views

app_name = 'Accueil'

urlpatterns = [
    path('', views.accueil, name='accueil')
]
