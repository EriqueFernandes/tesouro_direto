from django.urls import path
from . import views

urlpatterns = [
    path('attArquivo/', views.attArquivo, name="attArquivo"),
    path('', views.painel, name="painel"),
    path('grf/', views.grafico_movel, name="grafico")
]