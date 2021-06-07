from django.urls import path
from . import views

app_name = 'KDD99'

urlpatterns = [
    path('kdd99/', views.kdd99, name='kdd99')
]