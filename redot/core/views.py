from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .service.assinar_plano_svc import assinar_plano
from .service.salvar_pesquisa_svc import buscar_resultados_bd
from ..crawler.crawler.run_crawler import executar_todos_spiders as executar_spiders
from ..core.cron import pesquisa_atual

status_cron_data = {}

@csrf_exempt
@require_http_methods(["POST"])
def plano_assinado(request):
    """
    View para assinatura de planos
    """
    try:
        print("Dados recebidos:", request.body)
        data = json.loads(request.body)
        response, status_code = assinar_plano(data)
        return JsonResponse(response, status=status_code)
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def rota_crawler(request):
    """
    View para executar spiders do crawler
    """
    try:
        data = json.loads(request.body)
        nome_perfil = data.get('nome_perfil')

        if not nome_perfil:
            return JsonResponse({"erro": "nome_perfil é obrigatório"}, status=400)
        
        pesquisa_atual["nome_perfil"] = nome_perfil

        executar_spiders(nome_perfil)
        return JsonResponse({"mensagem": f"Spiders executadas para o perfil '{nome_perfil}'"}, status=200)

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def obter_resultados(request):
    """
    View para obter resultados das pesquisas
    """
    data = json.loads(request.body)
    nome_perfil = data.get('nome_perfil')

    if not nome_perfil:
        return JsonResponse({"erro": "Parâmetro 'nome_perfil' é obrigatório"}, status=400)
    
    try:

        resultados = buscar_resultados_bd(nome_perfil)
        return JsonResponse(resultados, safe=False)

    except Exception as e:
        return JsonResponse({
            "erro": str(e),
            "resultados": [],
            "total": 0,
            "status": "erro"
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def status_cron(request):
    """
    View para verificar status do cron
    """
    try:
        from .cron import obter_resultados
        resultados = obter_resultados()
        return JsonResponse(resultados)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

def obter_status_resultados():
    """
    Função auxiliar para obter status dos resultados
    Implemente conforme a lógica do seu sistema
    """
    return {
        "status": "ativo",
        "ultima_execucao": None,
        "detalhes": pesquisa_atual
    }