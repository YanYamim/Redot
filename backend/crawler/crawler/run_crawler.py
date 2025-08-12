from crawler.crawler.spiders.google_scrapy import GoogleSpider
from crawler.crawler.spiders.facebook_scrapy import FacebookSpider
from crawler.crawler.spiders.instagram_scrapy import InstagramSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def executar_spiders(nome_perfil, app):
    process = CrawlerProcess(get_project_settings())

    process.crawl(GoogleSpider, nome_perfil=nome_perfil, app_context=app.app_context)
    process.crawl(InstagramSpider, nome_perfil=nome_perfil, app_context=app.app_context)
    process.crawl(FacebookSpider, nome_perfil=nome_perfil, app_context=app.app_context)

    process.start()