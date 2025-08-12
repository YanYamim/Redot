import pytest
from scrapy.http import HtmlResponse, Request
from crawler.crawler.spiders.facebook_scrapy import FacebookSpider
from unittest.mock import patch

@pytest.fixture
def spider():
    return FacebookSpider(nome_perfil="perfil_teste")

def test_start_requests(spider):
    requests = list(spider.start_requests())
    assert len(requests) == 1

    req = requests[0]
    assert req.url == "https://www.facebook.com/perfil_teste/"
    assert req.headers[b'User-Agent'] == b'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    assert req.headers[b'Accept-Language'] == b'en-US,en;q=0.9'
    assert req.callback == spider.parse

@patch("crawler.crawler.spiders.facebook_scrapy.salvar_pesquisa")
def test_parse_com_titulo(mock_salvar, spider):
    html = "<html><head><title>Perfil Público</title></head><body></body></html>"
    request = Request(url="https://www.facebook.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html,
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_called_once_with({
        'nome_pesquisa': "perfil_teste",
        'nome_resultado': "Perfil Público",
        'fonte': "facebook",
        'url': "https://www.facebook.com/perfil_teste/"
    })

@patch("crawler.crawler.spiders.facebook_scrapy.salvar_pesquisa")
def test_parse_sem_titulo(mock_salvar, spider, caplog):
    html = "<html><head></head><body>Sem título</body></html>"
    request = Request(url="https://www.facebook.com/perfil_teste/")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html,
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_not_called()
    assert "Não foi possível extrair o título" in caplog.text
