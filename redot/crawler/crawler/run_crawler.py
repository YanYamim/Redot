from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from importlib import import_module
from ..crawler.spiders.google_scrapy import GoogleSpider
from ..crawler.spiders.facebook_scrapy import FacebookSpider
from ..crawler.spiders.instagram_scrapy import InstagramSpider
import django
from django.apps import apps
import threading

def _crawl_all(nome_perfil):
    """
    Executa todos os spiders em sequência usando CrawlerProcess
    """
    # Configura o Django para poder usar os models
    if not apps.ready:
        django.setup()
    
    # Usa as configurações existentes do seu settings.py
    settings_module = import_module('crawler.crawler.settings')
    settings = Settings()
    settings.setmodule(settings_module, priority='project')
    
    # Configurações adicionais para executar em sequência
    settings.set('CONCURRENT_REQUESTS', 1)
    settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 1)
    settings.set('DOWNLOAD_DELAY', 2)
    
    process = CrawlerProcess(settings)
    
    # Executa os spiders em sequência
    process.crawl(FacebookSpider, nome_perfil=nome_perfil)
    process.crawl(InstagramSpider, nome_perfil=nome_perfil)
    process.crawl(GoogleSpider, nome_perfil=nome_perfil)
    
    # Inicia o crawling (bloqueante)
    process.start()
    
    return {"status": "completed", "spiders": 3}

def executar_spiders(nome_perfil):
    """
    Função principal para executar todos os spiders em uma thread separada
    """
    # Garante que o Django está configurado
    if not apps.ready:
        django.setup()
    
    # Executa em uma thread separada para não bloquear
    def run_crawlers():
        try:
            return _crawl_all(nome_perfil)
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    # Inicia o crawling em uma thread separada
    thread = threading.Thread(target=run_crawlers)
    thread.daemon = True
    thread.start()
    
    # Retorna imediatamente enquanto o crawling roda em background
    return {"result": "started", "perfil": nome_perfil, "spiders_executados": 3, "status": "running_in_background"}