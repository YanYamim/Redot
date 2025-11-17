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
        self.logger.info(f"[FacebookSpider] Iniciando requests para: {self.start_urls}")
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Cache-Control': 'no-cache',
                },
                meta={'dont_retry': True, 'handle_httpstatus_all': True}
            )

    def parse(self, response):        
        if response.status != 200:
            self.logger.error(f"[FacebookSpider] Status {response.status} - Perfil não encontrado: {response.url}")
            raise CloseSpider('Perfil não encontrado')

        title = response.css('title::text').get()
        self.logger.info(f"[FacebookSpider] Título extraído: {title}")

        if not title or title.lower() in ['facebook', 'error', 'not found']:
            self.logger.error(f"[FacebookSpider] Título inválido ou página de erro: {title}")
            raise CloseSpider('Perfil não encontrado')

        data = {
            'nome_pesquisa': self.nome_perfil,
            'resultado': title.strip(),
            'fonte': 'facebook',
            'url': response.url
        }
        
        try:
            salvar_pesquisa(data)
                
        except Exception as e:
            self.logger.error(f"[FacebookSpider] Exceção ao salvar: {str(e)}")

    def errback(self, failure):
        self.logger.error(f"[FacebookSpider] Erro na requisição: {failure.value}")
        raise CloseSpider('Perfil não encontrado')