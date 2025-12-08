import scrapy
from scrapy.exceptions import CloseSpider
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com", "google.com.br"]
    
    def __init__(self, nome_perfil='', *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.google.com/search?q={nome_perfil}"]
        self.logger.info(f"[GoogleSpider] Iniciada para: {nome_perfil}")

    def start_requests(self):
        self.logger.info(f"[GoogleSpider] Iniciando requests para: {self.start_urls}")
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Cache-Control': 'no-cache',
                },
                meta={
                    'handle_httpstatus_all': True,
                    'dont_retry': True
                }
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"[GoogleSpider] Status {response.status} - Pesquisa falhou: {response.url}")
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': f'Erro na pesquisa Google - Status {response.status}',
                'fonte': 'google',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
            except Exception as e:
                self.logger.error(f"[GoogleSpider] Erro ao salvar pesquisa com erro: {str(e)}")
            return
        
        resultados = (response.css('div.g') | 
                     response.css('div.tF2Cxc') | 
                     response.css('[data-sokoban-container]') |
                     response.css('div.MjjYud'))
        
        self.logger.info(f"[GoogleSpider] Encontrados {len(resultados)} resultados")

        resultados_salvos = 0

        for i, resultado in enumerate(resultados[:5]):  
            title = self.extrair_titulo(resultado)
            link = self.extrair_link(resultado)

            if title and link:
                url_final = self.processar_url(link, response)
                
                data = {
                    'nome_pesquisa': self.nome_perfil,
                    'resultado': title.strip(),
                    'fonte': 'google',
                    'url': url_final,
                }

                try:
                    salvar_pesquisa(data)
                    resultados_salvos += 1
                    self.logger.info(f"[GoogleSpider] Resultado {i+1} salvo: {title[:50]}...")
                except Exception as e:
                    self.logger.error(f"[GoogleSpider] Erro ao salvar resultado {i+1}: {str(e)}")

        if resultados_salvos == 0:
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': f'Pesquisa Google: {self.nome_perfil} - Nenhum resultado encontrado',
                'fonte': 'google',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
                self.logger.info("[GoogleSpider] Pesquisa sem resultados salva")
            except Exception as e:
                self.logger.error(f"[GoogleSpider] Erro ao salvar pesquisa vazia: {str(e)}")

    def errback(self, failure):
        self.logger.error(f"[GoogleSpider] Erro na requisição: {failure.value}")
        
        data = {
            'nome_pesquisa': self.nome_perfil,
            'resultado': f'Erro na pesquisa Google: {str(failure.value)}',
            'fonte': 'google',
            'url': self.start_urls[0] if self.start_urls else ''
        }
        try:
            salvar_pesquisa(data)
        except Exception as e:
            self.logger.error(f"[GoogleSpider] Erro ao salvar pesquisa com falha: {str(e)}")
        
        raise CloseSpider('Erro na pesquisa Google')