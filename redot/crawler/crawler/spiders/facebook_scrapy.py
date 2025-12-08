import scrapy
from scrapy.exceptions import CloseSpider
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["facebook.com"]
    
    def __init__(self, nome_perfil='', *args, **kwargs):
        super(FacebookSpider, self).__init__(*args, **kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.facebook.com/{nome_perfil}"] 
        self.logger.info(f"[FacebookSpider] Iniciada para: {nome_perfil}")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                meta={'handle_httpstatus_all': True}
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"[FacebookSpider] Status {response.status}")
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': f'Erro ao buscar perfil Facebook - Status {response.status}',
                'fonte': 'facebook',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
            except Exception as e:
                self.logger.error(f"[FacebookSpider] Erro ao salvar: {str(e)}")
            return

        title = response.css('title::text').get()
        
        if title:
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': title.strip(),
                'fonte': 'facebook',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
                self.logger.info(f"[FacebookSpider] Perfil salvo: {title}")
            except Exception as e:
                self.logger.error(f"[FacebookSpider] Erro ao salvar: {str(e)}")

    def errback(self, failure):
        self.logger.error(f"[FacebookSpider] Erro: {failure.value}")
        data = {
            'nome_pesquisa': self.nome_perfil,
            'resultado': f'Erro na busca Facebook: {str(failure.value)}',
            'fonte': 'facebook',
            'url': ''
        }
        try:
            salvar_pesquisa(data)
        except Exception as e:
            self.logger.error(f"[FacebookSpider] Erro ao salvar falha: {str(e)}")