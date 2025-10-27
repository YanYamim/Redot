from django.urls import path
from . import views

urlpatterns = [
    path('usuario/cadastro', views.novo_usuario, name='novo_usuario'),
    path('login', views.autenticacao, name='autenticacao'),
]