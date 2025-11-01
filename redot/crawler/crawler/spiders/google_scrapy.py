import scrapy
import django
from django.apps import apps
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa

if not apps.ready:
    django.setup()

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]

    def __init__(self, nome_perfil='', app_context=None, **kwargs):
        super().__init__(**kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.google.com/search?q={nome_perfil}"]
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

    async def start(self):
        async for req in super().start():
            yield req

    def parse(self, response):
        resultados = response.css('div.g')

        if not resultados:
            self.logger.warning("Nenhum resultado encontrado. Pode ser bloqueio do Google.")

        for resultado in resultados:
            title = resultado.css('h3::text').get()
            url = resultado.css('a::attr(href)').get()

            if title and url:
                data = {
                    'nome_pesquisa': self.nome_perfil,
                    'nome_resultado': title.strip(),
                    'fonte': 'google',
                    'url': response.urljoin(url)
                }

                try:
                    self.logger.debug('GoogleSpider: encontrado item para %s: %s', self.nome_perfil, data.get('nome_resultado'))
                    if self.app_context:
                        with self.app_context():
                            salvar_pesquisa(data)
                    else:
                        salvar_pesquisa(data)
                    self.logger.info('GoogleSpider: item salvo para %s', self.nome_perfil)
                except Exception as e:
                    # Garantir que qualquer erro de persistência seja logado no stdout do crawler
                    self.logger.exception('GoogleSpider: erro ao salvar resultado para %s: %s', self.nome_perfil, e)

            else:
                self.logger.warning("Não foi possível extrair o título. A página pode estar protegida.")