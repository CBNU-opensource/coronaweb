from django.urls import path
from . import views

urlpatterns=[
    path('main/', views.main, name='main'),
    path('nations/', views.nations, name='nations'),
    path('regions/', views.regions, name='regions'),
    path('departure/', views.departure, name='departure'),
]