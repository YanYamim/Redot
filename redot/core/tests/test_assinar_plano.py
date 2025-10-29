from django.test import TestCase
from datetime import date, timedelta
from redot.core.service.assinar_plano_svc import assinar_plano
from redot.core.models import TipoPlano, Plano
from redot.accounts.models import User, Conta

class AssinarPlanoTestCase(TestCase):
    """Testes para assinatura de planos"""

    def setUp(self):
        """Configuração inicial dos testes"""
        self.usuario = User.objects.create(
            tipo='F',
            email='teste@email.com',
            nome_usuario='João Silva',
            cpf='12345678900'
        )

        self.conta = Conta.objects.create(
            id_usuario=self.usuario,
            login='joao.silva',
            senha='senha_hash',
            data_criacao=date.today()
        )

        self.plano_mensal = TipoPlano.objects.create(
            nome_tipo_plano='Plano Mensal Teste',
            preco=29.90,
            duracao_dias=30
        )

        self.plano_anual = TipoPlano.objects.create(
            nome_tipo_plano='Plano Anual Teste',
            preco=299.90,
            duracao_dias=365
        )

    def test_assinatura_plano_mensal_sucesso(self):
        """Testa assinatura de plano mensal com sucesso"""
        data = {
            'id_tipo_plano': self.plano_mensal.id_tipo_plano,
            'id_conta': self.conta.id_conta
        }

        resultado, status = assinar_plano(data)

        self.assertEqual(status, 200)
        self.assertEqual(resultado['id_tipo_plano'], self.plano_mensal.id_tipo_plano)
        self.assertEqual(resultado['id_conta'], self.conta.id_conta)
        self.assertTrue(resultado['ativa'])

        plano = Plano.objects.get(id_plano=resultado['id_plano'])
        self.assertIsNotNone(plano)
        self.assertEqual(plano.id_tipo_plano.id_tipo_plano, self.plano_mensal.id_tipo_plano)

    def test_assinatura_plano_anual_sucesso(self):
        """Testa assinatura de plano anual com sucesso"""
        data = {
            'id_tipo_plano': self.plano_anual.id_tipo_plano,
            'id_conta': self.conta.id_conta
        }

        resultado, status = assinar_plano(data)

        self.assertEqual(status, 200)
        self.assertEqual(resultado['id_tipo_plano'], self.plano_anual.id_tipo_plano)
        self.assertTrue(resultado['ativa'])

        data_inicio = date.fromisoformat(resultado['data_inicio'])
        data_fim = date.fromisoformat(resultado['data_fim'])
        
        self.assertEqual(data_inicio, date.today())
        self.assertEqual(data_fim, date.today() + timedelta(days=365))

    def test_assinatura_sem_id_tipo_plano(self):
        """Testa erro quando id_tipo_plano não é fornecido"""
        data = {
            'id_conta': self.conta.id_conta
        }

        resultado, status = assinar_plano(data)

        self.assertEqual(status, 400)
        self.assertIn('error', resultado)
        self.assertIn('obrigatórios', resultado['error'])

    def test_assinatura_sem_id_conta(self):
        """Testa erro quando id_conta não é fornecido"""
        data = {
            'id_tipo_plano': self.plano_mensal.id_tipo_plano
        }

        resultado, status = assinar_plano(data)

        self.assertEqual(status, 400)
        self.assertIn('error', resultado)
        self.assertIn('obrigatórios', resultado['error'])

    def test_assinatura_tipo_plano_inexistente(self):
        """Testa erro quando tipo de plano não existe"""
        data = {
            'id_tipo_plano': 9999,  
            'id_conta': self.conta.id_conta
        }

        resultado, status = assinar_plano(data)

        self.assertEqual(status, 404)
        self.assertIn('error', resultado)
        self.assertIn('não encontrado', resultado['error'])

    def test_plano_ativo_dentro_prazo(self):
        """Testa se plano permanece ativo dentro do prazo"""
        data = {
            'id_tipo_plano': self.plano_mensal.id_tipo_plano,
            'id_conta': self.conta.id_conta
        }

        resultado, status = assinar_plano(data)

        self.assertEqual(status, 200)
        self.assertTrue(resultado['ativa'])

        plano = Plano.objects.get(id_plano=resultado['id_plano'])
        self.assertTrue(plano.ativa)

    def test_multiplas_assinaturas_mesma_conta(self):
        """Testa que é possível ter múltiplas assinaturas para a mesma conta"""
        data1 = {
            'id_tipo_plano': self.plano_mensal.id_tipo_plano,
            'id_conta': self.conta.id_conta
        }
        resultado1, status1 = assinar_plano(data1)
        self.assertEqual(status1, 200)

        data2 = {
            'id_tipo_plano': self.plano_anual.id_tipo_plano,
            'id_conta': self.conta.id_conta
        }
        resultado2, status2 = assinar_plano(data2)
        self.assertEqual(status2, 200)

        planos = Plano.objects.filter(id_conta=self.conta)
        self.assertEqual(planos.count(), 2)

    def test_calculo_data_fim_correto(self):
        """Testa se a data de fim é calculada corretamente"""
        data = {
            'id_tipo_plano': self.plano_mensal.id_tipo_plano,
            'id_conta': self.conta.id_conta
        }

        resultado, status = assinar_plano(data)

        data_inicio = date.fromisoformat(resultado['data_inicio'])
        data_fim = date.fromisoformat(resultado['data_fim'])
        
        diferenca_dias = (data_fim - data_inicio).days
        
        self.assertEqual(diferenca_dias, self.plano_mensal.duracao_dias)
