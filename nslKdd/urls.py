from django.urls import path
from . import views

app_name = 'nslKdd'

urlpatterns = [
    path('nslkdd/', views.nslkdd, name='nslkdd')
]