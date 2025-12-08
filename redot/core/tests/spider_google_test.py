import pytest
from scrapy.http import HtmlResponse, Request
from redot.crawler.crawler.spiders.google_scrapy import GoogleSpider
from unittest.mock import patch 

@pytest.fixture
def spider():
    return GoogleSpider(nome_perfil="perfil_teste")

def test_start_requests(spider):
    """Testa se start_requests gera URLs corretas"""
    requests = list(spider.start_requests())
    assert len(requests) == 1

    req = requests[0]
    assert "perfil_teste" in req.url
    assert req.callback == spider.parse

@patch("redot.crawler.crawler.spiders.google_scrapy.salvar_pesquisa")
def test_parse_com_resultados(mock_salvar, spider):
    """Testa parse quando há resultados"""
    html = """<html>
                <body>
                    <div class="g">
                        <h3>Perfil Público</h3>
                        <a href="http://example.com">Link</a>
                    </div>
                    <div class="g">
                        <h3>Outro Resultado</h3>
                        <a href="http://outro.com">Link</a>
                    </div>
                </body>
            </html>
            """
    request = Request(url="https://www.google.com/search?q=perfil_teste")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html.encode('utf-8'),
        encoding='utf-8'
    )

    spider.parse(response)

    assert mock_salvar.call_count >= 1
    
    first_call = mock_salvar.call_args_list[0][0][0]
    assert first_call['nome_pesquisa'] == "perfil_teste"
    assert first_call['resultado'] == "Perfil Público"
    assert first_call['fonte'] == "google"

@patch("redot.crawler.crawler.spiders.google_scrapy.salvar_pesquisa")
def test_parse_sem_titulo(mock_salvar, spider):
    """Testa parse quando não há título - não salva"""
    html = """
            <html>
            <body>
                <div class="g">
                <a href="http://example.com"></a>
                </div>
            </body>
            </html>
            """
    request = Request(url="https://www.google.com/search?q=perfil_teste")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html.encode('utf-8'),
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_not_called()

@patch("redot.crawler.crawler.spiders.google_scrapy.salvar_pesquisa")
def test_parse_sem_resultados(mock_salvar, spider):
    """Testa parse quando não há resultados"""
    html = "<html><body><p>Nenhum resultado</p></body></html>"
    request = Request(url="https://www.google.com/search?q=perfil_teste")
    response = HtmlResponse(
        url=request.url,
        request=request,
        body=html.encode('utf-8'),
        encoding='utf-8'
    )

    spider.parse(response)

    mock_salvar.assert_not_called()