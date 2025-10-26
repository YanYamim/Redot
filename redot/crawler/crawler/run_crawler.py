import crochet
crochet.setup()

from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from importlib import import_module
from twisted.internet import defer
from crawler.crawler.spiders.google_scrapy import GoogleSpider
from crawler.crawler.spiders.facebook_scrapy import FacebookSpider
from crawler.crawler.spiders.instagram_scrapy import InstagramSpider
import django
from django.apps import apps

@crochet.run_in_reactor
def _crawl_all(nome_perfil):
    """
    Executa todos os spiders em paralelo usando as configurações existentes
    """
    if not apps.ready:
        django.setup()
    
    settings_module = import_module('crawler.crawler.settings')
    settings: Settings = Settings()
    settings.setmodule(settings_module, priority='project')
    
    runner = CrawlerRunner(settings)
    
    deferred_crawls = [
        runner.crawl(FacebookSpider, nome_perfil=nome_perfil),
        runner.crawl(InstagramSpider, nome_perfil=nome_perfil),
        runner.crawl(GoogleSpider, nome_perfil=nome_perfil),
    ]
    return defer.DeferredList(deferred_crawls, fireOnOneErrback=False, consumeErrors=False)

def executar_spiders(nome_perfil):
    """
    Função principal para executar todos os spiders
    """
    if not apps.ready:
        django.setup()
    
    eventual = _crawl_all(nome_perfil)
    results = eventual.wait(timeout=1800) 

    failures = []
    for succeeded, payload in results:
        if not succeeded:
            try:
                failures.append(str(payload.value))
            except Exception:
                failures.append(repr(payload))

    if failures:
        raise Exception("; ".join(failures))

    return {"result": "ok", "perfil": nome_perfil, "spiders_executados": 3}