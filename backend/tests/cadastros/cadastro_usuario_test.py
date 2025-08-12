import pytest
from unittest.mock import patch, MagicMock
from services import cadastrar_usuario_service

@pytest.fixture
def fake_usuario():
    usuario = MagicMock()
    usuario.to_dict.return_value = {
        'email': 'teste@email.com',
        'tipo': 'F',
        'cpf': '12345678900'
    }
    return usuario

def test_cadastro_pf_sucesso(fake_usuario):
    data = {
        'email': 'teste@email.com',
        'tipo': 'F',
        'cpf': '12345678900',
        'nome_usuario': 'João'
    }

    with patch('services.cadastrar_usuario_service.Usuario') as MockUsuario, \
         patch('services.cadastrar_usuario_service.db') as mock_db, \
         patch('services.cadastrar_usuario_service.cadastrar_conta') as mock_conta:
        
        MockUsuario.query.filter_by.return_value.first.return_value = None

        MockUsuario.return_value = fake_usuario
        mock_conta.return_value = True

        result, status = cadastrar_usuario_service.cadastrar_usuario(data)

        assert status == 201
        assert result['email'] == data['email']

def test_cadastro_pj_sucesso(fake_usuario):
    data = {
        'email': 'teste@email.com',
        'tipo': 'J',
        'cnpj': '12345678000190',
        'razao_social': 'Empresa X'
    }

    with patch('services.cadastrar_usuario_service.Usuario') as MockUsuario, \
         patch('services.cadastrar_usuario_service.db') as mock_db, \
         patch('services.cadastrar_usuario_service.cadastrar_conta') as mock_conta:
        
        MockUsuario.query.filter_by.return_value.first.return_value = None
        MockUsuario.return_value = fake_usuario
        mock_conta.return_value = True

        result, status = cadastrar_usuario_service.cadastrar_usuario(data)

        assert status == 201
        assert result['email'] == data['email']

def test_cadastro_pf_falha_criar_conta(fake_usuario):
    data = {
        'email': 'falha@email.com',
        'tipo': 'F',
        'cpf': '123.456.789-00',
        'nome_usuario': 'Erro PF'
    }

    with patch('services.cadastrar_usuario_service.Usuario') as MockUsuario, \
         patch('services.cadastrar_usuario_service.db') as mock_db, \
         patch('services.cadastrar_usuario_service.cadastrar_conta') as mock_conta:

        MockUsuario.query.filter_by.return_value.first.return_value = None
        MockUsuario.return_value = fake_usuario
        mock_conta.return_value = False

        result, status = cadastrar_usuario_service.cadastrar_usuario(data)

        assert status == 500
        assert 'Erro ao criar conta' in result['error']

def test_cadastro_pj_falha_criar_conta(fake_usuario):
    data = {
        'email': 'falha@email.com',
        'tipo': 'J',
        'cpf': '12.345.678/0001-90',
        'nome_usuario': 'Erro PF'
    }

    with patch('services.cadastrar_usuario_service.Usuario') as MockUsuario, \
         patch('services.cadastrar_usuario_service.db') as mock_db, \
         patch('services.cadastrar_usuario_service.cadastrar_conta') as mock_conta:

        MockUsuario.query.filter_by.return_value.first.return_value = None
        MockUsuario.return_value = fake_usuario
        mock_conta.return_value = False

        result, status = cadastrar_usuario_service.cadastrar_usuario(data)

        assert status == 500
        assert 'Erro ao criar conta' in result['error']

def test_email_ja_cadastrado():
    data = {
        'email': 'existe@email.com',
        'tipo': 'F'
    }

    with patch('services.cadastrar_usuario_service.Usuario') as MockUsuario:
        MockUsuario.query.filter_by.return_value.first.return_value = True

        result, status = cadastrar_usuario_service.cadastrar_usuario(data)

        assert status == 400
        assert result['error'] == 'Email já cadastrado'