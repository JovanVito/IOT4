from django.urls import path
from . import views

urlpatterns = [
    path('antrean/ambil/', views.ambil_antrean, name='ambil_antrean'),
    path('antrean/status/', views.status_antrean, name='status_antrean'),
    path('antrean/panggil/', views.panggil_antrean, name='panggil_antrean'),
    path('antrean/reset/', views.reset_antrean, name='reset_antrean'), 
]