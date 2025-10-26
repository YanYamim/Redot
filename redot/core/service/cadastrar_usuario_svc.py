from django.db import transaction
import re
import traceback
from ..models import Usuario
from .cadastrar_conta_svc import cadastrar_conta

def cadastrar_usuario(data):
    try:
        if Usuario.objects.filter(email=data['email']).exists():
            return {'error': 'Email já cadastrado'}, 400

        if data['tipo'] == 'F':
            identificacao = re.sub(r'\D', '', data.get('cpf', ''))
        elif data['tipo'] == 'J':
            identificacao = re.sub(r'\D', '', data.get('cnpj', ''))

        with transaction.atomic():
            novo_usuario = Usuario(
                tipo=data['tipo'],
                email=data['email'],
                rg=data.get('rg'),
                telefone=data.get('telefone'),
                celular=data.get('celular'),
                cep=data.get('cep'),
                n=data.get('numero'),
                complemento=data.get('complemento'),
                id_role=data.get('id_role', 1)
            )

            if data['tipo'] == 'F':
                novo_usuario.nome_usuario = data.get('nome_usuario')
                novo_usuario.cpf = identificacao
            else:
                novo_usuario.razao_social = data.get('razao_social')
                novo_usuario.cnpj = identificacao

            novo_usuario.save()

            conta = cadastrar_conta(novo_usuario, data)
            if not conta:
                return {'error': 'Erro ao criar conta'}, 500

            return novo_usuario.to_dict(), 201

    except Exception as e:
        print("Erro ao cadastrar usuário:", traceback.format_exc())
        return {'error': str(e)}, 500