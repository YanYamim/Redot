import pytest
import logging
from unittest.mock import patch, MagicMock

from redot.core.cron import (
    start_scrapy,
    ultimos_resultados,
    pesquisa_atual,
)


@pytest.fixture(autouse=True)
def reset_state():
    """Reseta o estado global antes de cada teste."""
    ultimos_resultados.update({
        'dados': None,
        'ultima_execucao': None,
        'status': 'Aguardando primeira execução'
    })
    pesquisa_atual["nome_perfil"] = None
    yield


def test_start_scrapy_sem_nome(caplog):
    """Sem nome definido, deve apenas logar e não executar spiders."""
    with caplog.at_level(logging.WARNING):
        start_scrapy("minutalmente")
    
    assert "Nenhum perfil definido" in caplog.text
    assert ultimos_resultados["status"] == "Aguardando primeira execução"


@patch('redot.core.cron.CrawlerProcess')
def test_start_scrapy_com_sucesso(mock_crawler_process):
    """Com nome definido e execução ok, deve atualizar ultimos_resultados."""
    mock_instance = MagicMock()
    mock_crawler_process.return_value = mock_instance
    
    pesquisa_atual["nome_perfil"] = "perfil_teste"

    start_scrapy("diariamente")

    mock_crawler_process.assert_called_once()
    
    assert ultimos_resultados["status"] == "Sucesso"
    assert ultimos_resultados["ultima_execucao"] is not None
    assert ultimos_resultados["dados"] == {'status': 'completo'}


@patch('redot.core.cron.CrawlerProcess')
def test_start_scrapy_erro(mock_crawler_process):
    """Em caso de erro do executor, status deve refletir o erro."""
    mock_crawler_process.side_effect = Exception("erro mockado")
    
    pesquisa_atual["nome_perfil"] = "perfil_teste"

    start_scrapy("mensalmente")

    assert ultimos_resultados["dados"] is None
    assert "Erro: erro mockado" in ultimos_resultados["status"]
    assert ultimos_resultados["ultima_execucao"] is not None