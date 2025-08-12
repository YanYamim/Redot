import pytest
from unittest.mock import patch, MagicMock
from cron.cron_crawler import start_crawler, start_scrapy, ultimos_resultados, pesquisa_atual
from apscheduler.schedulers.background import BackgroundScheduler
import time

@pytest.fixture(autouse=True)
def reset_state():
    ultimos_resultados.update({
        'dados': None,
        'ultima_execucao': None,
        'status': 'Aguardando primeira execução'
    })
    pesquisa_atual["nome_perfil"] = None
    yield

def test_start_scrapy_sem_nome(capfd):
    start_scrapy("minutalmente", app=MagicMock())
    out, _ = capfd.readouterr()
    assert "Nenhum termo para pesquisar" in out
    assert ultimos_resultados["status"] == "Aguardando primeira execução"

@patch("cron.cron_crawler.executar_spiders")
def test_start_scrapy_com_sucesso(mock_executar):
    pesquisa_atual["nome_perfil"] = "perfil_teste"
    mock_executar.return_value = {"result": "ok"}

    start_scrapy("diariamente", app=MagicMock())

    assert ultimos_resultados["dados"] == {"result": "ok"}
    assert ultimos_resultados["status"] == "Sucesso"
    assert ultimos_resultados["ultima_execucao"] is not None

@patch("cron.cron_crawler.executar_spiders")
def test_start_scrapy_erro(mock_executar):
    pesquisa_atual["nome_perfil"] = "perfil_teste"
    mock_executar.side_effect = Exception("erro mockado")

    start_scrapy("mensalmente", app=MagicMock())

    assert "Erro: erro mockado" in ultimos_resultados["status"]

def test_start_crawler_agenda_jobs():
    app_mock = MagicMock()
    scheduler = BackgroundScheduler()

    with patch("cron.cron_crawler.BackgroundScheduler", return_value=scheduler):
        start_crawler(app_mock)
        job_names = [job.name for job in scheduler.get_jobs()]
        assert set(job_names) == {"crawl_minutal", "crawl_diario", "crawl_semanal", "crawl_mensal"}

def test_cron_job_executa_eventualmente():
    scheduler = BackgroundScheduler()
    mock_func = MagicMock()

    scheduler.add_job(mock_func, 'interval', seconds=1, id="teste_job")
    scheduler.start()

    time.sleep(2.5)

    scheduler.shutdown(wait=False)

    assert mock_func.call_count >= 1

@patch("cron.cron_crawler.start_scrapy")
def test_cron_ativa_start_scrapy_por_minuto(mock_start_scrapy):
    scheduler = BackgroundScheduler()
    app_mock = MagicMock()

    scheduler.add_job(mock_start_scrapy, 'interval', seconds=1, id="teste_job", args=["minutalmente", app_mock])
    scheduler.start()

    time.sleep(2.5)
    scheduler.shutdown(wait=False)

    assert mock_start_scrapy.called