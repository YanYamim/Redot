from models import db, Usuario
from services.cadastrar_conta_service import cadastrar_conta
import re
import traceback

def cadastrar_usuario(data):
    if Usuario.query.filter_by(email=data['email']).first():
        return {'error': 'Email já cadastrado'}, 400

    if data['tipo'] == 'F':
        identificacao = re.sub(r'\D', '', data.get('cpf', ''))
    elif data['tipo'] == 'J':
        identificacao = re.sub(r'\D', '', data.get('cnpj', ''))

    try:
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

        db.session.add(novo_usuario)
        db.session.commit()

        conta = cadastrar_conta(novo_usuario, data)
        if not conta:
            return {'error': 'Erro ao criar conta'}, 500

        return novo_usuario.to_dict(), 201

    except Exception as e:
        db.session.rollback()
        print("Erro ao cadastrar usuário:", traceback.format_exc())
        return {'error': str(e)}, 500
