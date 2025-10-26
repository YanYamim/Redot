from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class RadarViewTestCase(TestCase):
    def test_post_sem_nome_perfil(self):
        resp = self.client.post('/radar', data={}, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('nome_perfil', resp.json().get('erro', ''))

    @patch('redot.core.views.executar_spiders', return_value={})
    def test_post_com_nome_perfil_ok(self, _mock_exec):
        payload = {"nome_perfil": "empresa_teste"}
        resp = self.client.post('/radar', data=payload, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('mensagem', resp.json())
