import scrapy

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["facebook.com"]
    
    def __init__(self, nome_perfil='', *args, **kwargs):
        super(FacebookSpider, self).__init__(*args, **kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.facebook.com/{nome_perfil}"]  # Remova a barra final
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
                meta={'dont_retry': True}
            )

    def parse(self, response):
        self.logger.info(f"[FacebookSpider] Resposta recebida. Status: {response.status}")
        
        if response.status == 200:
            title = response.css('title::text').get()
            self.logger.info(f"[FacebookSpider] Título extraído: {title}")

            if title and title.lower() not in ['facebook', 'error', 'not found']:
                data = {
                    'nome_pesquisa': self.nome_perfil,
                    'resultado': title.strip(),
                    'fonte': 'facebook',
                    'url': response.url
                }

                self.logger.info(f"[FacebookSpider] Tentando salvar dados...")
                
                try:
                    from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa_thread
                    resultado, status = salvar_pesquisa_thread(data)
                    
                    if status == 200:
                        self.logger.info(f"[FacebookSpider] ✅ Processo de salvamento iniciado em thread")
                    else:
                        self.logger.error(f"[FacebookSpider] ❌ Erro ao iniciar salvamento: {resultado}")
                        
                except Exception as e:
                    self.logger.error(f"[FacebookSpider] ❌ Exceção ao salvar: {str(e)}")
            else:
                self.logger.warning(f"[FacebookSpider] Título inválido ou página de erro: {title}")
        else:
            self.logger.warning(f"[FacebookSpider] Status {response.status} - Não foi possível acessar")

    def errback(self, failure):
        self.logger.error(f"[FacebookSpider] ❌ Erro na requisição: {failure.value}")