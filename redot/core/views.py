import json
import threading
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from scrapy.crawler import CrawlerProcess

from .service.assinar_plano_svc import assinar_plano
from .service.salvar_pesquisa_svc import buscar_resultados_bd
from ..core.cron import pesquisa_atual

from redot.crawler.crawler.spiders.instagram_scrapy import InstagramSpider
from redot.crawler.crawler.spiders.google_scrapy import GoogleSpider
from redot.crawler.crawler.spiders.facebook_scrapy import FacebookSpider

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
    """View para executar spiders"""
    try:
        data = json.loads(request.body)
        nome_perfil = data.get('nome_perfil')

        if not nome_perfil:
            return JsonResponse({"erro": "nome_perfil obrigatório"}, status=400)
        
        # Executa em threads
        def _run_crawler():
            try:
                process = CrawlerProcess({
                    'BOT_NAME': 'crawler',
                    'CONCURRENT_REQUESTS': 1,
                    'DOWNLOAD_DELAY': 2,
                })
                process.crawl(InstagramSpider, nome_perfil=nome_perfil)
                process.crawl(GoogleSpider, nome_perfil=nome_perfil)
                process.crawl(FacebookSpider, nome_perfil=nome_perfil)
                process.start()
            except Exception as e:
                print(f"Erro ao executar crawler: {str(e)}")
                import traceback
                traceback.print_exc()
        
        thread = threading.Thread(target=_run_crawler, daemon=True)
        thread.start()
        
        return JsonResponse({
            "status": "iniciado",
            "mensagem": f"Crawler iniciado para {nome_perfil}"
        }, status=202)
    
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def obter_resultados(request):
    """
    View para obter resultados das pesquisas
    """
    nome_perfil = request.GET.get('nome_perfil')


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