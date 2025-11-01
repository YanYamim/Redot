import scrapy
import django
from django.apps import apps
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa

if not apps.ready:
    django.setup()

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["facebook.com"]

    def __init__(self, nome_perfil='', app_context=None, **kwargs):
        super().__init__(**kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.facebook.com/{nome_perfil}/"]
        self.app_context = app_context

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Accept-Language': 'en-US,en;q=0.9',
                },
                callback=self.parse
            )

    def parse(self, response):
        title = response.css('title::text').get()

        if title:
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': title.strip(),
                'fonte': 'facebook',
                'url': response.url
            }

            try:
                print(f"[FacebookSpider] salvando item para {self.nome_perfil}: {data.get('resultado')}")
                self.logger.debug('FacebookSpider: encontrado item para %s: %s', self.nome_perfil, data.get('resultado'))
                if self.app_context:
                    with self.app_context():
                        salvar_pesquisa(data)
                else:
                    salvar_pesquisa(data)
                print(f"[FacebookSpider] salvou item para {self.nome_perfil}")
                self.logger.info('FacebookSpider: item salvo para %s', self.nome_perfil)
            except Exception as e:
                print(f"[FacebookSpider] erro ao salvar para {self.nome_perfil}: {e}")
                self.logger.exception('FacebookSpider: erro ao salvar resultado para %s: %s', self.nome_perfil, e)

        else:
            self.logger.warning("Não foi possível extrair o título. A página pode estar protegida.")