import crochet
crochet.setup()

from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from importlib import import_module
from twisted.internet import defer
from crawler.crawler.spiders.google_scrapy import GoogleSpider
from crawler.crawler.spiders.facebook_scrapy import FacebookSpider
from crawler.crawler.spiders.instagram_scrapy import InstagramSpider

@crochet.run_in_reactor
def _crawl_all(nome_perfil, app_context):
    settings_module = import_module('crawler.crawler.settings')
    settings: Settings = Settings()
    settings.setmodule(settings_module, priority='project')
    runner = CrawlerRunner(settings)
    deferred_crawls = [
        runner.crawl(FacebookSpider, nome_perfil=nome_perfil, app_context=app_context),
        runner.crawl(InstagramSpider, nome_perfil=nome_perfil, app_context=app_context),
        runner.crawl(GoogleSpider, nome_perfil=nome_perfil, app_context=app_context),
    ]
    return defer.DeferredList(deferred_crawls, fireOnOneErrback=False, consumeErrors=False)

def executar_spiders(nome_perfil, app):
    eventual = _crawl_all(nome_perfil, app.app_context)
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

    return {"result": "ok"}