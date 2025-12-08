import scrapy
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    
    def __init__(self, nome_perfil='', *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.instagram.com/{nome_perfil}/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                meta={'download_timeout': 30}
            )

    def parse(self, response):
        """Parse da página do Instagram"""
        if response.status != 200:
            self.logger.error(f"[InstagramSpider] Status {response.status}")
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': f'Perfil não encontrado - Status {response.status}',
                'fonte': 'instagram',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
            except Exception as e:
                self.logger.error(f"[InstagramSpider] Erro ao salvar: {str(e)}")
            return

        title = response.css('title::text').get()
        
        if title:
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': title.strip(),
                'fonte': 'instagram',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
                self.logger.info(f"[InstagramSpider] Perfil salvo: {title}")
            except Exception as e:
                self.logger.error(f"[InstagramSpider] Erro ao salvar: {str(e)}")

    def errback(self, failure):
        """Trata erros de requisição"""
        self.logger.error(f"[InstagramSpider] Erro: {failure.value}")
        data = {
            'nome_pesquisa': self.nome_perfil,
            'resultado': f'Erro na busca: {str(failure.value)}',
            'fonte': 'instagram',
            'url': ''
        }
        try:
            salvar_pesquisa(data)
        except Exception as e:
            self.logger.error(f"[InstagramSpider] Erro ao salvar falha: {str(e)}")