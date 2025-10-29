import pytest
from datetime import date
from redot.accounts.models import User, Conta
from redot.accounts.service.autenticar_usuario_svc import (
    login_usuario,
    gerar_token_jwt,
    verificar_jwt_token,
    obter_usuario_por_token,
)


@pytest.fixture
def user_conta(db):
    """Cria um usuário e sua conta associados para uso nos testes."""
    user = User.objects.create_user(
        username='teste_user',
        email='teste@email.com',
        password='senha123',
        tipo='F',
        nome_usuario='Usuário Teste',
        cpf='12345678901',
    )
    conta = Conta.objects.create(
        id_usuario=user,
        login='teste@email.com',
        data_criacao=date.today(),
    )
    conta.set_senha('senha123')
    conta.save()
    return user, conta


@pytest.mark.django_db
def test_login_com_email_e_senha_corretos(user_conta):
    user, conta = user_conta
    resultado, status_code = login_usuario('teste@email.com', 'senha123')

    assert status_code == 200
    assert 'token' in resultado
    assert 'usuario' in resultado
    assert 'conta_id' in resultado
    assert resultado['message'] == 'Login realizado com sucesso'
    assert resultado['conta_id'] == conta.id_conta

    assert resultado['token'] is not None
    assert isinstance(resultado['token'], str)

    assert resultado['usuario']['email'] == 'teste@email.com'
    assert resultado['usuario']['username'] == 'teste_user'
    assert 'senha' not in resultado['usuario']
    assert 'password' not in resultado['usuario']


@pytest.mark.django_db
def test_login_com_login_direto(user_conta):
    _user, _conta = user_conta
    resultado, status_code = login_usuario('teste@email.com', 'senha123')
    assert status_code == 200
    assert 'token' in resultado


@pytest.mark.django_db
def test_login_com_senha_incorreta(user_conta):
    _user, _conta = user_conta
    resultado, status_code = login_usuario('teste@email.com', 'senha_errada')
    assert status_code == 401
    assert 'erro' in resultado
    assert resultado['erro'] == 'Senha incorreta'


@pytest.mark.django_db
def test_login_com_usuario_inexistente(db):
    resultado, status_code = login_usuario('naoexiste@email.com', 'senha123')
    assert status_code == 404
    assert 'erro' in resultado
    assert resultado['erro'] == 'Usuário não encontrado'


@pytest.mark.django_db
def test_login_com_email_vazio(db):
    resultado, status_code = login_usuario('', 'senha123')
    assert status_code == 404
    assert 'erro' in resultado


@pytest.mark.django_db
def test_gerar_e_verificar_token_jwt(user_conta):
    user, conta = user_conta
    token = gerar_token_jwt(conta.id_conta, user.id)
    assert token is not None
    assert isinstance(token, str)

    payload = verificar_jwt_token(token)
    assert 'error' not in payload
    assert payload['conta_id'] == conta.id_conta
    assert payload['usuario_id'] == user.id
    assert 'exp' in payload and 'iat' in payload


@pytest.mark.django_db
def test_verificar_token_invalido(db):
    token_invalido = 'token.invalido.teste'
    payload = verificar_jwt_token(token_invalido)
    assert 'error' in payload
    assert payload['error'] == 'Token inválido'


@pytest.mark.django_db
def test_obter_usuario_por_token_valido(user_conta):
    user, conta = user_conta
    token = gerar_token_jwt(conta.id_conta, user.id)
    usuario, error = obter_usuario_por_token(token)
    assert error is None
    assert usuario is not None
    assert usuario.id == user.id
    assert usuario.email == 'teste@email.com'


@pytest.mark.django_db
def test_obter_usuario_por_token_invalido(db):
    token_invalido = 'token.invalido.teste'
    usuario, error = obter_usuario_por_token(token_invalido)
    assert usuario is None
    assert error is not None
    assert 'error' in error
    assert error['error'] == 'Token inválido'


@pytest.mark.django_db
def test_conta_check_senha_com_hash_correto(user_conta):
    _user, conta = user_conta
    assert conta.check_senha('senha123') is True
    assert conta.check_senha('senha_errada') is False


@pytest.mark.django_db
def test_conta_set_senha_gera_hash(user_conta):
    user, _conta = user_conta
    nova_conta = Conta.objects.create(
        id_usuario=user,
        login='nova_conta',
        data_criacao=date.today(),
    )
    nova_conta.set_senha('nova_senha')
    nova_conta.save()
    assert nova_conta.senha != 'nova_senha'
    assert nova_conta.check_senha('nova_senha') is True


@pytest.mark.django_db
def test_multiplos_usuarios_e_contas(user_conta):
    _user1, conta1 = user_conta
    user2 = User.objects.create_user(
        username='user2',
        email='user2@email.com',
        password='pass456',
        tipo='J',
        razao_social='Empresa Teste',
    )
    conta2 = Conta.objects.create(
        id_usuario=user2,
        login='user2@email.com',
        data_criacao=date.today(),
    )
    conta2.set_senha('pass456')
    conta2.save()

    resultado1, status1 = login_usuario('teste@email.com', 'senha123')
    assert status1 == 200 and resultado1['conta_id'] == conta1.id_conta

    resultado2, status2 = login_usuario('user2@email.com', 'pass456')
    assert status2 == 200 and resultado2['conta_id'] == conta2.id_conta

    assert resultado1['token'] != resultado2['token']


@pytest.mark.django_db
def test_usuario_sem_conta_nao_pode_logar(db):
    User.objects.create_user(
        username='sem_conta',
        email='sem_conta@email.com',
        password='senha999',
    )
    resultado, status = login_usuario('sem_conta@email.com', 'senha999')
    assert status == 404 and 'erro' in resultado

