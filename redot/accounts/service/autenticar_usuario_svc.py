import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ..models import User, Conta
import traceback

def gerar_token_jwt(conta_id, usuario_id):
    """Gera um token JWT para o usuário autenticado"""
    payload = {
        'conta_id': conta_id,
        'usuario_id': usuario_id,
        'exp': datetime.utcnow() + getattr(settings, 'JWT_EXPIRATION_DELTA', timedelta(days=7)),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(
        payload, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token

def verificar_jwt_token(token):
    """Verifica a validade do token JWT"""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expirado'}
    except jwt.InvalidTokenError:
        return {'error': 'Token inválido'}
    
def login_usuario(login, senha):
    """
    Autentica um usuário com login/email e senha
    Retorna o token JWT e dados do usuário se bem-sucedido
    """

    try:
        conta = Conta.objects.filter(login=login).first()
        
        if not conta:
            usuario = User.objects.filter(email=login).first()
            if usuario:
                conta = Conta.objects.filter(id_usuario=usuario).first()
        
        if not conta:
            return {"erro": "Usuário não encontrado"}, 404
        
        if not conta.check_senha(senha):
            return {"erro": "Senha incorreta"}, 401

        token = gerar_token_jwt(conta.id_conta, conta.id_usuario.id)

        usuario_data = conta.id_usuario.to_dict()
        usuario_data.pop('senha', None)

        return {
            'token': token,
            'usuario': usuario_data,
            'conta_id': conta.id_conta,
            'message': 'Login realizado com sucesso'
        }, 200
    
    except Exception:
        print("Erro na autenticação:", traceback.format_exc())
        return {'error': 'Erro interno no servidor'}, 500
    
def obter_usuario_por_token(token):
    """Obtém o usuário associado a um token JWT"""

    try:
        payload = verificar_jwt_token(token)

        if 'error' in payload:
            return None, payload

        usuario_id = payload.get('usuario_id')
        conta_id = payload.get('conta_id')

        usuario = User.objects.filter(id=usuario_id).first()
        conta = Conta.objects.filter(id_conta=conta_id).first()

        if not usuario or not conta:
            return None, {'error': 'Usuário não encontrado'}    

        return usuario, None
    
    except Exception:
        print("Erro ao obter usuário por token:", traceback.format_exc())
        return None, {'error': 'Erro ao validar token'}
