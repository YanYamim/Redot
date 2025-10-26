import scrapy
import django
from django.apps import apps

from core.service.salvar_pesquisa_svc import salvar_pesquisa

if not apps.ready:
    django.setup()

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["facebook.com"]
    
    def __init__(self, nome_perfil='', **kwargs):
        super().__init__(**kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.facebook.com/{nome_perfil}/"]

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
        title = response.css('title::text').get()

        if title and "facebook" in title.lower():
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': title.strip(),
                'fonte': 'facebook',
                'url': response.url
            }

            try:
                salvar_pesquisa(data)
            except Exception as e:
                self.logger.error(f"Facebook - Erro ao salvar: {str(e)}")
        else:
            self.logger.warning("Facebook - Não foi possível extrair título válido")

    def errback(self, failure):
        self.logger.error(f"Facebook - Erro na requisição: {failure.value}")