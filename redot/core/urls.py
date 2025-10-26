from django.urls import path
from . import views

urlpatterns = [
    path('planos/pagamento', views.plano_assinado, name='plano_assinado'),
    
    path('radar', views.rota_crawler, name='rota_crawler'),
    path('radar/resultados', views.obter_resultados, name='obter_resultados'),
    path('radar/status', views.status_cron, name='status_cron'),
    
    path('usuario/cadastro', views.novo_usuario, name='novo_usuario'),
    path('login', views.autenticacao, name='autenticacao'),
]