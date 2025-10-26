import pytest
from unittest.mock import patch

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


def test_start_scrapy_sem_nome(capfd):
    """Sem nome definido, deve apenas logar e não executar spiders."""
    start_scrapy("minutalmente")
    out, _ = capfd.readouterr()
    assert "Nenhum termo para pesquisar" in out
    assert ultimos_resultados["status"] == "Aguardando primeira execução"


@patch("redot.core.cron.executar_spiders")
def test_start_scrapy_com_sucesso(mock_executar):
    """Com nome definido e execução ok, deve atualizar ultimos_resultados."""
    pesquisa_atual["nome_perfil"] = "perfil_teste"
    mock_executar.return_value = {"result": "ok"}

    start_scrapy("diariamente")

    assert ultimos_resultados["dados"] == {"result": "ok"}
    assert ultimos_resultados["status"] == "Sucesso"
    assert ultimos_resultados["ultima_execucao"] is not None


@patch("redot.core.cron.executar_spiders")
def test_start_scrapy_erro(mock_executar):
    """Em caso de erro do executor, status deve refletir o erro."""
    pesquisa_atual["nome_perfil"] = "perfil_teste"
    mock_executar.side_effect = Exception("erro mockado")

    start_scrapy("mensalmente")

    assert ultimos_resultados["dados"] is None
    assert "Erro: erro mockado" in ultimos_resultados["status"]