import json
from django.test import TestCase, Client
from unittest.mock import patch, MagicMock


class RadarViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_post_sem_nome_perfil(self):
        """Testa POST sem o parâmetro nome_perfil"""
        resp = self.client.post(
            '/radar',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('nome_perfil', resp.json().get('erro', ''))

    @patch('redot.core.views.CrawlerProcess')
    def test_post_com_nome_perfil_ok(self, mock_crawler_process):
        """Testa POST com nome_perfil válido"""
        mock_instance = MagicMock()
        mock_crawler_process.return_value = mock_instance
        
        payload = json.dumps({"nome_perfil": "empresa_teste"})
        resp = self.client.post(
            '/radar',
            data=payload,
            content_type='application/json'
        )
        
        self.assertEqual(resp.status_code, 202)
        self.assertEqual(resp.json()['status'], 'iniciado')
        self.assertIn('empresa_teste', resp.json()['mensagem'])

    def test_post_json_invalido(self):
        """Testa POST com JSON inválido"""
        resp = self.client.post(
            '/radar',
            data='json inválido',
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('JSON inválido', resp.json().get('erro', ''))