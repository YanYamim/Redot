"""
URL configuration for redot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas de assinatura
    path('planos/pagamento', views.plano_assinado, name='plano_assinado'),
    
    # Rotas de radar/crawler
    path('radar', views.rota_crawler, name='rota_crawler'),
    path('radar/resultados', views.obter_resultados, name='obter_resultados'),
    path('radar/status', views.status_cron, name='status_cron'),
    
    # Rotas de usuário
    path('usuario/cadastro', views.novo_usuario, name='novo_usuario'),
    path('login', views.autenticacao, name='autenticacao'),
]
