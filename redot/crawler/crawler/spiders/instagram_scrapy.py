import scrapy
from scrapy.exceptions import CloseSpider
from redot.core.service.salvar_pesquisa_svc import salvar_pesquisa
from urllib.parse import quote, unquote
import re

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["google.com"]
    
    def __init__(self, nome_perfil='', *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        self.nome_perfil = nome_perfil
        self.start_urls = [f"https://www.google.com/search?q=site:instagram.com+{quote(nome_perfil)}"]
        self.logger.info(f"[InstagramSpider] Buscando perfil: {nome_perfil}")

    def start_requests(self):
        self.logger.info(f"[InstagramSpider] Iniciando requests para: {self.start_urls}")
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
                meta={'handle_httpstatus_all': True}
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"[InstagramSpider] Status {response.status}")
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': f'Erro ao buscar perfil Instagram - Status {response.status}',
                'fonte': 'instagram',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
            except Exception as e:
                self.logger.error(f"[InstagramSpider] Erro ao salvar: {str(e)}")
            return

        resultados = response.css('div.g, div.tF2Cxc, [data-sokoban-container]')
        self.logger.info(f"[InstagramSpider] Encontrados {len(resultados)} resultados")

        perfis_encontrados = 0

        for resultado in resultados[:3]:
            title = resultado.css('h3::text, [role="heading"]::text').get()
            link = resultado.css('a::attr(href)').get()

            if title and link and 'instagram.com' in link:
                url_final = self.processar_url(link, response)
                nome_perfil_extraido = self.extrair_nome_perfil(url_final)
                
                # Estrutura COMPATÍVEL com o service
                data = {
                    'nome_pesquisa': self.nome_perfil,
                    'resultado': nome_perfil_extraido or title.strip(),
                    'fonte': 'instagram',
                    'url': url_final
                }

                try:
                    salvar_pesquisa(data)
                    perfis_encontrados += 1
                    self.logger.info(f"[InstagramSpider] Perfil encontrado: {data['resultado']}")
                except Exception as e:
                    self.logger.error(f"[InstagramSpider] Erro ao salvar: {str(e)}")

        if perfis_encontrados == 0:
            data = {
                'nome_pesquisa': self.nome_perfil,
                'resultado': f'Nenhum perfil Instagram encontrado para: {self.nome_perfil}',
                'fonte': 'instagram',
                'url': response.url
            }
            try:
                salvar_pesquisa(data)
            except Exception as e:
                self.logger.error(f"[InstagramSpider] Erro ao salvar pesquisa vazia: {str(e)}")

    def processar_url(self, link, response):
        if link.startswith('/url?'):
            try:
                from urllib.parse import parse_qs
                parsed_url = parse_qs(link[5:])
                actual_url = parsed_url.get('q', [link])[0]
                return unquote(actual_url)
            except Exception:
                return response.urljoin(link)
        else:
            return response.urljoin(link)

    def extrair_nome_perfil(self, url):
        """Extrai nome do perfil do URL do Instagram"""
        match = re.search(r'instagram\.com/([^/?]+)', url)
        return match.group(1) if match else None

    def errback(self, failure):
        self.logger.error(f"[InstagramSpider] Erro: {failure.value}")
        data = {
            'nome_pesquisa': self.nome_perfil,
            'resultado': f'Erro na busca Instagram: {str(failure.value)}',
            'fonte': 'instagram',
            'url': ''
        }
        try:
            salvar_pesquisa(data)
        except Exception as e:
            self.logger.error(f"[InstagramSpider] Erro ao salvar falha: {str(e)}")
        raise CloseSpider('Erro na busca')