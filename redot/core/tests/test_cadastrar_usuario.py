from django.test import TestCase
from datetime import date
from redot.core.service.cadastrar_usuario_svc import cadastrar_usuario
from redot.core.models import Usuario, Conta


class CadastroUsuarioTestCase(TestCase):
    """Testes para cadastro de usuário"""

    def setUp(self):
        """Configuração inicial dos testes"""
        self.data_pf = {
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

        self.data_pj = {
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

    def test_cadastro_pf_sucesso(self):
        """Testa cadastro de pessoa física com sucesso (sem mocks)."""
        resultado, status = cadastrar_usuario(self.data_pf)

        self.assertEqual(status, 201)
        self.assertEqual(resultado['email'], self.data_pf['email'])
        self.assertEqual(resultado['tipo'], 'F')
        self.assertEqual(resultado['cpf'], '12345678900')  # Sem formatação

        usuario = Usuario.objects.get(email=self.data_pf['email'])
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nome_usuario, 'João Silva')

        conta = Conta.objects.get(login=self.data_pf['email'])
        self.assertEqual(conta.id_usuario.id_usuario, usuario.id_usuario)

    def test_cadastro_pj_sucesso(self):
        """Testa cadastro de pessoa jurídica com sucesso (sem mocks)."""
        resultado, status = cadastrar_usuario(self.data_pj)

        self.assertEqual(status, 201)
        self.assertEqual(resultado['email'], self.data_pj['email'])
        self.assertEqual(resultado['tipo'], 'J')
        self.assertEqual(resultado['cnpj'], '12345678000190')  # Sem formatação

        usuario = Usuario.objects.get(email=self.data_pj['email'])
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.razao_social, 'Empresa X LTDA')

        conta = Conta.objects.get(login=self.data_pj['email'])
        self.assertEqual(conta.id_usuario.id_usuario, usuario.id_usuario)

    def test_email_ja_cadastrado(self):
        """Testa erro quando email já está cadastrado (fluxo real)."""
        cadastrar_usuario(self.data_pf)

        resultado, status = cadastrar_usuario(self.data_pf)

        self.assertEqual(status, 400)
        self.assertIn('error', resultado)
        self.assertEqual(resultado['error'], 'Email já cadastrado')

    def test_cadastro_pf_falha_criar_conta(self):
        """Testa falha ao criar conta para PF criando conflito de login (sem mocks)."""
        usuario_ocupante = Usuario.objects.create(
            tipo='F', email='ocupante@example.com', nome_usuario='Ocupante', cpf='00000000000'
        )
        Conta.objects.create(
            id_usuario=usuario_ocupante,
            login=self.data_pf['email'],  
            senha='hash',
            data_criacao=date.today()
        )

        resultado, status = cadastrar_usuario(self.data_pf)

        self.assertEqual(status, 500)
        self.assertIn('error', resultado)
        self.assertIn('Erro ao criar conta', resultado['error'])

    def test_cadastro_pj_falha_criar_conta(self):
        """Testa falha ao criar conta para PJ criando conflito de login (sem mocks)."""
        usuario_ocupante = Usuario.objects.create(
            tipo='F', email='ocupante2@example.com', nome_usuario='Ocupante 2', cpf='11111111111'
        )
        Conta.objects.create(
            id_usuario=usuario_ocupante,
            login=self.data_pj['email'],
            senha='hash',
            data_criacao=date.today()
        )

        resultado, status = cadastrar_usuario(self.data_pj)

        self.assertEqual(status, 500)
        self.assertIn('error', resultado)
        self.assertIn('Erro ao criar conta', resultado['error'])

    def test_cpf_formatado_removido(self):
        """Testa se a formatação do CPF é removida corretamente (sem mocks)."""
        resultado, status = cadastrar_usuario(self.data_pf)

        self.assertEqual(status, 201)
        self.assertEqual(resultado['cpf'], '12345678900')
        self.assertNotIn('.', resultado['cpf'])
        self.assertNotIn('-', resultado['cpf'])

    def test_cnpj_formatado_removido(self):
        """Testa se a formatação do CNPJ é removida corretamente (sem mocks)."""
        resultado, status = cadastrar_usuario(self.data_pj)

        self.assertEqual(status, 201)
        self.assertEqual(resultado['cnpj'], '12345678000190')
        self.assertNotIn('.', resultado['cnpj'])
        self.assertNotIn('-', resultado['cnpj'])
        self.assertNotIn('/', resultado['cnpj'])
