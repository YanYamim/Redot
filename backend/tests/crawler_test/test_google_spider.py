import pytest
from scrapy.http import HtmlResponse, Request
from crawler.crawler.spiders.google_scrapy import GoogleSpider
from unittest.mock import patch 

@pytest.fixture
def spider():
    return GoogleSpider(nome_perfil="perfil_teste")

def test_start_requests(spider):
    requests = list(spider.start_requests())
    assert len(requests) == 1

    req = requests[0]
    assert req.url == "https://www.google.com/search?q=perfil_teste"
    assert req.headers[b'User-Agent'] == b'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    assert req.headers[b'Accept-Language'] == b'en-US,en;q=0.9'
    assert req.callback == spider.parse

@patch("crawler.crawler.spiders.google_scrapy.salvar_pesquisa")
def test_parse_com_titulo(mock_salvar, spider):
    html = """<html>
                <body>
                    <div class="g">
                    <a href="/url?url=http://example.com">
                        <h3>Perfil Público</h3>
                    </a>
                    </div>
                </body>
                </html>
            """
    request = Request(url="https://www.google.com/search?q=perfil_teste")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html,
        encoding='utf-8'
    )

    spider.nome_perfil = "perfil_teste" 
    spider.parse(response)

    mock_salvar.assert_called_once_with({
        'nome_pesquisa': "perfil_teste",
        'nome_resultado': "Perfil Público",
        'fonte': "google",
        'url': "https://www.google.com/url?url=http://example.com"
    })

@patch("crawler.crawler.spiders.google_scrapy.salvar_pesquisa")
def test_parse_sem_titulo(mock_salvar, spider, caplog):
    html = """
            <html>
            <body>
                <div class="g">
                <a href="/url?url=http://example.com"></a>
                </div>
            </body>
            </html>
            """
    request = Request(url="https://www.google.com/search?q=perfil_teste")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html,
        encoding='utf-8'
    )

    spider.nome_perfil = "perfil_teste"
    with caplog.at_level("WARNING"):
        spider.parse(response)

    mock_salvar.assert_not_called()
    assert "Não foi possível extrair o título" in caplog.text
