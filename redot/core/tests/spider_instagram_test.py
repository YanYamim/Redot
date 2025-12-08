import pytest
from scrapy.http import HtmlResponse, Request
from redot.crawler.crawler.spiders.instagram_scrapy import InstagramSpider
from unittest.mock import patch

@pytest.fixture
def spider():
    return InstagramSpider(nome_perfil="perfil_teste")

def test_start_requests(spider):
    """Testa se start_requests gera URLs corretas"""
    requests = list(spider.start_requests())
    assert len(requests) == 1

    req = requests[0]
    assert req.url == "https://www.instagram.com/perfil_teste/"
    assert req.callback == spider.parse

@patch("redot.crawler.crawler.spiders.instagram_scrapy.salvar_pesquisa")
def test_parse_com_titulo(mock_salvar, spider):
    """Testa parse quando há título na página"""
    html = "<html><head><title>Perfil Público</title></head><body></body></html>"
    request = Request(url="https://www.instagram.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html.encode('utf-8'),
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_called_once()
    call_args = mock_salvar.call_args[0][0]
    assert call_args['nome_pesquisa'] == "perfil_teste"
    assert call_args['resultado'] == "Perfil Público"
    assert call_args['fonte'] == "instagram"
    assert call_args['url'] == "https://www.instagram.com/perfil_teste/"

@patch("redot.crawler.crawler.spiders.instagram_scrapy.salvar_pesquisa")
def test_parse_sem_titulo(mock_salvar, spider):
    """Testa parse quando não há título"""
    html = "<html><head></head><body>Sem título</body></html>"
    request = Request(url="https://www.instagram.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html.encode('utf-8'),
        encoding='utf-8'
    )

    spider.parse(response)

    # Não deve chamar se não houver título
    mock_salvar.assert_not_called()

@patch("redot.crawler.crawler.spiders.instagram_scrapy.salvar_pesquisa")
def test_parse_status_erro(mock_salvar, spider):
    """Testa parse quando status é erro"""
    request = Request(url="https://www.instagram.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=b"<html></html>",
        status=404,
        encoding='utf-8'
    )

    spider.parse(response)

    # Deve chamar com erro
    mock_salvar.assert_called_once()
    call_args = mock_salvar.call_args[0][0]
    assert "Perfil não encontrado" in call_args['resultado']
    assert call_args['fonte'] == "instagram"