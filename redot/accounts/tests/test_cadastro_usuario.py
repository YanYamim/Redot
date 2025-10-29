import pytest
from datetime import date
from redot.accounts.service.cadastrar_usuario_svc import cadastrar_usuario
from redot.accounts.models import User, Conta


@pytest.fixture
def data_pf():
    return {
        'email': 'teste@email.com',
        'tipo': 'F',
        'cpf': '123.456.789-00',
        'nome_usuario': 'João Silva',
        'rg': '123456789',
        'telefone': '1122334455',
        'celular': '11987654321',
        'cep': '12345678',
        'numero': 100,
        'complemento': 'Apto 10',
        'senha': 'senha123'
    }


@pytest.fixture
def data_pj():
    return {
        'email': 'empresa@email.com',
        'tipo': 'J',
        'cnpj': '12.345.678/0001-90',
        'razao_social': 'Empresa X LTDA',
        'rg': None,
        'telefone': '1122334455',
        'celular': None,
        'cep': '12345678',
        'numero': 200,
        'complemento': 'Sala 5',
        'senha': 'senha456'
    }


@pytest.mark.django_db
def test_cadastro_pf_sucesso(data_pf):
    resultado, status = cadastrar_usuario(data_pf)

    assert status == 201
    assert resultado['email'] == data_pf['email']
    assert resultado['tipo'] == 'F'
    assert resultado['cpf'] == '12345678900'

    usuario = User.objects.get(email=data_pf['email'])
    assert usuario is not None
    assert usuario.nome_usuario == 'João Silva'

    conta = Conta.objects.get(login=data_pf['email'])
    assert conta.id_usuario.id == usuario.id


@pytest.mark.django_db
def test_cadastro_pj_sucesso(data_pj):
    resultado, status = cadastrar_usuario(data_pj)

    assert status == 201
    assert resultado['email'] == data_pj['email']
    assert resultado['tipo'] == 'J'
    assert resultado['cnpj'] == '12345678000190'

    usuario = User.objects.get(email=data_pj['email'])
    assert usuario is not None
    assert usuario.razao_social == 'Empresa X LTDA'

    conta = Conta.objects.get(login=data_pj['email'])
    assert conta.id_usuario.id == usuario.id


@pytest.mark.django_db
def test_email_ja_cadastrado(data_pf):
    cadastrar_usuario(data_pf)
    resultado, status = cadastrar_usuario(data_pf)

    assert status == 400
    assert 'error' in resultado
    assert resultado['error'] == 'Email já cadastrado'


@pytest.mark.django_db
def test_cadastro_pf_falha_criar_conta(data_pf):
    usuario_ocupante = User.objects.create(
        tipo='F',
        email='ocupante@example.com',
        username='ocupante@example.com',
        nome_usuario='Ocupante',
        cpf='00000000000'
    )
    Conta.objects.create(
        id_usuario=usuario_ocupante,
        login=data_pf['email'],
        senha='hash',
        data_criacao=date.today()
    )

    resultado, status = cadastrar_usuario(data_pf)

    assert status == 500
    assert 'error' in resultado


@pytest.mark.django_db
def test_cadastro_pj_falha_criar_conta(data_pj):
    usuario_ocupante = User.objects.create(
        tipo='F',
        email='ocupante2@example.com',
        username='ocupante2@example.com',
        nome_usuario='Ocupante 2',
        cpf='11111111111'
    )
    Conta.objects.create(
        id_usuario=usuario_ocupante,
        login=data_pj['email'],
        senha='hash',
        data_criacao=date.today()
    )

    resultado, status = cadastrar_usuario(data_pj)

    assert status == 500
    assert 'error' in resultado


@pytest.mark.django_db
def test_cpf_formatado_removido(data_pf):
    resultado, status = cadastrar_usuario(data_pf)

    assert status == 201
    assert resultado['cpf'] == '12345678900'
    assert '.' not in resultado['cpf']
    assert '-' not in resultado['cpf']


@pytest.mark.django_db
def test_cnpj_formatado_removido(data_pj):
    resultado, status = cadastrar_usuario(data_pj)

    assert status == 201
    assert resultado['cnpj'] == '12345678000190'
    assert '.' not in resultado['cnpj']
    assert '-' not in resultado['cnpj']
    assert '/' not in resultado['cnpj']

