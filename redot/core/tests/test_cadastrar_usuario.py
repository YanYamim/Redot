"""
Testes para o serviço de cadastro de usuário
"""
from django.test import TestCase
from unittest.mock import patch, MagicMock
from redot.core.service.cadastrar_usuario_svc import cadastrar_usuario
from redot.core.models import Usuario


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
        """Testa cadastro de pessoa física com sucesso"""
        with patch('redot.core.service.cadastrar_usuario_svc.cadastrar_conta') as mock_conta:
            mock_conta.return_value = True

            resultado, status = cadastrar_usuario(self.data_pf)

            self.assertEqual(status, 201)
            self.assertEqual(resultado['email'], self.data_pf['email'])
            self.assertEqual(resultado['tipo'], 'F')
            self.assertEqual(resultado['cpf'], '12345678900')  # Sem formatação
            
            # Verifica se o usuário foi salvo
            usuario = Usuario.objects.get(email=self.data_pf['email'])
            self.assertIsNotNone(usuario)
            self.assertEqual(usuario.nome_usuario, 'João Silva')

    def test_cadastro_pj_sucesso(self):
        """Testa cadastro de pessoa jurídica com sucesso"""
        with patch('redot.core.service.cadastrar_usuario_svc.cadastrar_conta') as mock_conta:
            mock_conta.return_value = True

            resultado, status = cadastrar_usuario(self.data_pj)

            self.assertEqual(status, 201)
            self.assertEqual(resultado['email'], self.data_pj['email'])
            self.assertEqual(resultado['tipo'], 'J')
            self.assertEqual(resultado['cnpj'], '12345678000190')  # Sem formatação
            
            # Verifica se o usuário foi salvo
            usuario = Usuario.objects.get(email=self.data_pj['email'])
            self.assertIsNotNone(usuario)
            self.assertEqual(usuario.razao_social, 'Empresa X LTDA')

    def test_email_ja_cadastrado(self):
        """Testa erro quando email já está cadastrado"""
        # Primeiro cadastro
        with patch('redot.core.service.cadastrar_usuario_svc.cadastrar_conta') as mock_conta:
            mock_conta.return_value = True
            cadastrar_usuario(self.data_pf)

        # Tentativa de cadastro duplicado
        resultado, status = cadastrar_usuario(self.data_pf)

        self.assertEqual(status, 400)
        self.assertIn('error', resultado)
        self.assertEqual(resultado['error'], 'Email já cadastrado')

    def test_cadastro_pf_falha_criar_conta(self):
        """Testa falha ao criar conta para pessoa física"""
        with patch('redot.core.service.cadastrar_usuario_svc.cadastrar_conta') as mock_conta:
            mock_conta.return_value = False

            resultado, status = cadastrar_usuario(self.data_pf)

            self.assertEqual(status, 500)
            self.assertIn('error', resultado)
            self.assertIn('Erro ao criar conta', resultado['error'])

    def test_cadastro_pj_falha_criar_conta(self):
        """Testa falha ao criar conta para pessoa jurídica"""
        with patch('redot.core.service.cadastrar_usuario_svc.cadastrar_conta') as mock_conta:
            mock_conta.return_value = False

            resultado, status = cadastrar_usuario(self.data_pj)

            self.assertEqual(status, 500)
            self.assertIn('error', resultado)
            self.assertIn('Erro ao criar conta', resultado['error'])

    def test_cpf_formatado_removido(self):
        """Testa se a formatação do CPF é removida corretamente"""
        with patch('redot.core.service.cadastrar_usuario_svc.cadastrar_conta') as mock_conta:
            mock_conta.return_value = True

            resultado, status = cadastrar_usuario(self.data_pf)

            self.assertEqual(status, 201)
            # CPF deve estar sem pontos e traços
            self.assertEqual(resultado['cpf'], '12345678900')
            self.assertNotIn('.', resultado['cpf'])
            self.assertNotIn('-', resultado['cpf'])

    def test_cnpj_formatado_removido(self):
        """Testa se a formatação do CNPJ é removida corretamente"""
        with patch('redot.core.service.cadastrar_usuario_svc.cadastrar_conta') as mock_conta:
            mock_conta.return_value = True

            resultado, status = cadastrar_usuario(self.data_pj)

            self.assertEqual(status, 201)
            # CNPJ deve estar sem pontos, traços e barra
            self.assertEqual(resultado['cnpj'], '12345678000190')
            self.assertNotIn('.', resultado['cnpj'])
            self.assertNotIn('-', resultado['cnpj'])
            self.assertNotIn('/', resultado['cnpj'])
