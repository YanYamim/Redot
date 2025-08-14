import scrapy
from services.salvar_pesquisa_service import salvar_pesquisa

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    
    def __init__(self, nome_perfil='', app_context=None, **kwargs):
        super().__init__(**kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.instagram.com/{nome_perfil}/"]
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
                'fonte': 'instagram',
                'url': response.url
            }

            if self.app_context:
                with self.app_context():
                    salvar_pesquisa(data)
            else:
                salvar_pesquisa(data)

        else:
            self.logger.warning("Não foi possível extrair o título. A página pode estar protegida.")
