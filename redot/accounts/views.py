from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from ..accounts.service.cadastrar_usuario_svc import cadastrar_usuario
from ..accounts.service.autenticar_usuario_svc import login_usuario, obter_usuario_por_token

@csrf_exempt
@require_http_methods(["POST"])
def novo_usuario(request):
    """
    View para cadastro de novo usuário
    """
    try:
        data = json.loads(request.body)
        
        resultado, status_code = cadastrar_usuario(data)
        
        return JsonResponse(resultado, status=status_code, safe=False)
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'JSON inválido'}, 
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'error': 'Erro interno do servidor'}, 
            status=500
        )

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
            return JsonResponse(
                {'status': 'error', 'message': 'Email e senha são obrigatórios'}, 
                status=400
            )
        
        resultado, status_code = login_usuario(email, senha)
        
        return JsonResponse(resultado, status=status_code)
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'JSON inválido'}, 
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': 'Erro interno do servidor'}, 
            status=500
        )
    
@csrf_exempt
@require_http_methods(["GET"])
def perfil_usuario(request):
    """
    Exemplo de view que requer autenticação
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Token não fornecido'}, status=401)
    
    token = auth_header.split(' ')[1]
    usuario, error = obter_usuario_por_token(token)
    
    if error:
        return JsonResponse(error, status=401)
    
    return JsonResponse({
        'status': 'success',
        'usuario': usuario.to_dict()
    })
