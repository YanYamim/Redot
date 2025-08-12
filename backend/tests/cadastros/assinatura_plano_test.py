import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock
from services import assinar_plano_service
from types import SimpleNamespace

@pytest.fixture
def fake_plano():
    plano = MagicMock()
    plano.id_tipo_plano = 1 
    plano.to_dict.return_value = {
        "id_tipo_plano": 1,
        "data_inicio": date(2025, 1, 1),
        "data_fim": date(2025, 12, 31),
        "ativa": True
    }
    return plano

def test_assinatura_plano_sucesso(fake_plano):
    data = {
        "data_inicio": date(2025, 1, 1),
        "data_fim": date(2025, 12, 31),
    }

    with patch('services.assinar_plano_service.Tipo_Plano') as MockTipoPlano, \
         patch('services.assinar_plano_service.Plano') as MockPlano, \
         patch('services.assinar_plano_service.db') as mock_db:
        
        mock_tipo = MagicMock()
        mock_tipo.duracao_dias = 365
        MockTipoPlano.query.get.return_value = mock_tipo

        mock_nova_assinatura = MagicMock()
        mock_nova_assinatura.id_tipo_plano = fake_plano.id_tipo_plano
        mock_nova_assinatura.data_inicio = data["data_inicio"]
        mock_nova_assinatura.data_fim = data["data_fim"]
        mock_nova_assinatura.ativa = True
        MockPlano.return_value = mock_nova_assinatura

        resultado = assinar_plano_service.assinar_plano(fake_plano, data)

        assert resultado is mock_nova_assinatura
        assert resultado.ativa is True
        mock_db.session.add.assert_called_once_with(mock_nova_assinatura)
        mock_db.session.commit.assert_called_once()

def test_assinatura_plano_falha(fake_plano):
    data = {}  

    with patch('services.assinar_plano_service.Tipo_Plano') as MockTipoPlano, \
         patch('services.assinar_plano_service.db') as mock_db:
        
        mock_tipo = MagicMock()
        mock_tipo.duracao_dias = 365
        MockTipoPlano.query.get.return_value = mock_tipo

        resultado = assinar_plano_service.assinar_plano(fake_plano, data)

        assert resultado is None
        mock_db.session.rollback.assert_called_once()


def test_plano_ainda_ativo():
    tipo_plano = SimpleNamespace(duracao_dias=30)
    data_inicio = date.today() - timedelta(days=5)

    assinatura = SimpleNamespace(
        tipo_plano=tipo_plano,
        data_inicio=data_inicio,
        ativa=True
    )

    data_expiracao = data_inicio + timedelta(days=tipo_plano.duracao_dias)
    assinatura.ativa = not (date.today() > data_expiracao)

    assert assinatura.ativa is True

def test_plano_expirado():
    tipo_plano = SimpleNamespace(duracao_dias=10)
    data_inicio = date.today() - timedelta(days=15)

    assinatura = SimpleNamespace(
        tipo_plano=tipo_plano,
        data_inicio=data_inicio,
        ativa=True
    )

    data_expiracao = data_inicio + timedelta(days=tipo_plano.duracao_dias)
    assinatura.ativa = not (date.today() > data_expiracao)

    assert assinatura.ativa is False