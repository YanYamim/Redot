import scrapy
import urllib.parse

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    
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
                }
            )

    def parse(self, response):
        self.logger.info(f"[GoogleSpider] Resposta recebida. Status: {response.status}")
        
        # Tente diferentes seletores do Google
        resultados = response.css('div.g') or response.css('div.tF2Cxc') or response.css('[data-sokoban-container]')
        self.logger.info(f"[GoogleSpider] Encontrados {len(resultados)} resultados")

        if not resultados:
            # Salva pelo menos a pesquisa mesmo sem resultados
            data = {
                'nome_pesquisa': self.nome_perfil,
                'nome_resultado': f'Pesquisa Google: {self.nome_perfil}',
                'fonte': 'google',
                'url': response.url
            }
            
            try:
                from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa_thread
                resultado, status = salvar_pesquisa_thread(data)
                self.logger.info(f"[GoogleSpider] ✅ Pesquisa salva (sem resultados detalhados)")
            except Exception as e:
                self.logger.error(f"[GoogleSpider] ❌ Erro ao salvar pesquisa: {str(e)}")
            return

        for i, resultado in enumerate(resultados[:3]):
            title = resultado.css('h3::text, [role="heading"]::text').get()
            link = resultado.css('a::attr(href)').get()

            if title and link:
                if link.startswith('/url?'):
                    parsed_url = urllib.parse.urlparse(link)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    actual_url = query_params.get('q', [link])[0]
                else:
                    actual_url = link

                data = {
                    'nome_pesquisa': self.nome_perfil,
                    'nome_resultado': title.strip(),
                    'fonte': 'google',
                    'url': response.urljoin(actual_url)
                }

                try:
                    from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa_thread
                    resultado, status = salvar_pesquisa_thread(data)
                    
                    if status == 200:
                        self.logger.info(f"[GoogleSpider] ✅ Resultado {i+1} sendo salvo em thread")
                    else:
                        self.logger.error(f"[GoogleSpider] ❌ Erro ao salvar: {resultado}")
                        
                except Exception as e:
                    self.logger.error(f"[GoogleSpider] ❌ Exceção: {str(e)}")

    def errback(self, failure):
        self.logger.error(f"[GoogleSpider] ❌ Erro na requisição: {failure.value}")