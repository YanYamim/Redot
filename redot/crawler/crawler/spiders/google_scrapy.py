import scrapy
import django
from django.apps import apps
import urllib.parse

from core.service.salvar_pesquisa_svc import salvar_pesquisa

if not apps.ready:
    django.setup()

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    
    def __init__(self, nome_perfil='', **kwargs):
        super().__init__(**kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.google.com/search?q={nome_perfil}"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                },
                callback=self.parse,
                errback=self.errback,
                meta={'proxy': 'http://Mavi__fz8CY-country-US:Xman2025Mavip=PB@dc.oxylabs.io:8000'}
            )

    def parse(self, response):
        resultados = response.css('div.g') or response.css('[data-sokoban-container]')

        if not resultados:
            self.logger.warning("⚠️ Google - Nenhum resultado encontrado")
            return

        resultados_salvos = 0
        for resultado in resultados[:3]:  
            title = resultado.css('h3::text, [role="heading"] span::text').get()
            url = resultado.css('a::attr(href)').get()

            if title and url:
                if url.startswith('/url?'):
                    parsed_url = urllib.parse.urlparse(url)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    actual_url = query_params.get('q', [url])[0]
                else:
                    actual_url = url

                data = {
                    'nome_pesquisa': self.nome_perfil,
                    'resultado': title.strip(),
                    'fonte': 'google',
                    'url': response.urljoin(actual_url)
                }

                try:
                    salvar_pesquisa(data)
                    resultados_salvos += 1
                except Exception as e:
                    self.logger.error(f"Google - Erro ao salvar: {str(e)}")

        self.logger.info(f"Google - Total de resultados salvos: {resultados_salvos}")

    def errback(self, failure):
        self.logger.error(f"Google - Erro na requisição: {failure.value}")