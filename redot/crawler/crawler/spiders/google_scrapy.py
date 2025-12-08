import scrapy
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com", "google.com.br"]
    
    def __init__(self, nome_perfil='', *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.google.com/search?q={nome_perfil}"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                meta={'download_timeout': 30}
            )

    def parse(self, response):
        """Parse dos resultados do Google"""
        resultados = response.css('div.g')
        
        for resultado in resultados[:5]:
            titulo = resultado.css('h3::text').get()
            link = resultado.css('a::attr(href)').get()
            
            if titulo and link:
                data = {
                    'nome_pesquisa': self.nome_perfil,
                    'resultado': titulo.strip(),
                    'fonte': 'google',
                    'url': link
                }
                try:
                    salvar_pesquisa(data)
                    self.logger.info(f"[GoogleSpider] Resultado salvo: {titulo}")
                except Exception as e:
                    self.logger.error(f"[GoogleSpider] Erro ao salvar: {str(e)}")

    def errback(self, failure):
        """Trata erros de requisição"""
        self.logger.error(f"[GoogleSpider] Erro: {failure.value}")