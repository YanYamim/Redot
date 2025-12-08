import pytest
from scrapy.http import HtmlResponse, Request
from redot.crawler.crawler.spiders.facebook_scrapy import FacebookSpider
from unittest.mock import patch

@pytest.fixture
def spider():
    return FacebookSpider(nome_perfil="perfil_teste")


def test_start_requests(spider):
    """Testa se start_requests gera URLs corretas"""
    requests = list(spider.start_requests())
    assert len(requests) == 1
    assert "perfil_teste" in requests[0].url


@patch("redot.crawler.crawler.spiders.facebook_scrapy.salvar_pesquisa")
def test_parse_com_titulo(mock_salvar, spider):
    """Testa parse quando há título na página"""
    html = "<html><head><title>Perfil Público</title></head><body></body></html>"
    request = Request(url="https://www.facebook.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html.encode('utf-8'),
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_called_once()
    call_args = mock_salvar.call_args[0][0]
    assert call_args['resultado'] == "Perfil Público"


@patch("redot.crawler.crawler.spiders.facebook_scrapy.salvar_pesquisa")
def test_parse_sem_titulo(mock_salvar, spider):
    """Testa parse quando não há título"""
    html = "<html><head></head><body></body></html>"
    request = Request(url="https://www.facebook.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html.encode('utf-8'),
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_not_called()


@patch("redot.crawler.crawler.spiders.facebook_scrapy.salvar_pesquisa")
def test_parse_status_erro(mock_salvar, spider):
    """Testa parse quando status é erro"""
    request = Request(url="https://www.facebook.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=b"<html></html>",
        status=404,
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_called_once()
    call_args = mock_salvar.call_args[0][0]
    assert "Erro ao buscar perfil" in call_args['resultado']