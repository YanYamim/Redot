import scrapy
from scrapy.exceptions import CloseSpider
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    
    def __init__(self, nome_perfil='', *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.instagram.com/{nome_perfil}/"]
        self.logger.info(f"[InstagramSpider] Iniciada para: {nome_perfil}")

    def start_requests(self):
        self.logger.info(f"[InstagramSpider] Iniciando requests para: {self.start_urls}")
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                },
                meta={'handle_httpstatus_all': True}
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"[InstagramSpider] Status {response.status} - Perfil não encontrado: {response.url}")
            raise CloseSpider('Perfil não encontrado')
        
        title = response.css('title::text').get()
        self.logger.info(f"[InstagramSpider] Título extraído: {title}")

        if title:
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': title.strip(),
                'fonte': 'instagram',
                'url': response.url
            }

            self.logger.info("[InstagramSpider] Tentando salvar dados...")
            try:
                salvar_pesquisa(data)
            except Exception as e:
                self.logger.error(f"[InstagramSpider] Exceção ao salvar: {str(e)}")

    def errback(self, failure):
        self.logger.error(f"[InstagramSpider] Erro na requisição: {failure.value}")
        raise CloseSpider('Perfil não encontrado')