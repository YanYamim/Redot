from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Importações dos serviços (ajuste conforme sua estrutura)
from service.assinar_plano_svc import assinar_plano
from service.cadastrar_usuario_svc import cadastrar_usuario
from service.autenticar_usuario_svc import login_usuario
from service.salvar_pesquisa_svc import buscar_resultados_bd
from crawler.crawler.run_crawler import executar_spiders
from core.cron import pesquisa_atual

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
        return JsonResponse({"mensagem": f"Spiders executadas para o perfil '{nome_perfil}'"}), 200
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def obter_resultados(request):
    """
    View para obter resultados das pesquisas
    """
    try:
        data = json.loads(request.body)
        nome_perfil = data.get('nome_perfil')
        
        if not nome_perfil:
            return JsonResponse({"erro": "Parâmetro 'nome_perfil' é obrigatório"}, status=400)
        
        resultados = buscar_resultados_bd(nome_perfil)
        return JsonResponse(resultados, safe=False)
            
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
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
        from cron import obter_resultados
        resultados = obter_resultados()
        return JsonResponse(resultados)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def novo_usuario(request):
    """
    View para cadastro de novo usuário
    """
    try:
        data = json.loads(request.body)
        response, status_code = cadastrar_usuario(data)
        
        # Se a resposta já for um dicionário, retorne como JsonResponse
        if isinstance(response, dict):
            return JsonResponse(response, status=status_code)
        else:
            return response
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def autenticacao(request):
    """
    View para autenticação de usuário
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        senha = data.get('senha')
        
        if not email or not senha:
            return JsonResponse({"erro": "Email e senha são obrigatórios"}, status=400)
        
        response, status_code = login_usuario(email, senha)
        
        if isinstance(response, dict):
            return JsonResponse(response, status=status_code)
        else:
            return response
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
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