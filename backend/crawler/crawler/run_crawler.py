from scrapy.crawler import CrawlerProcess
from threading import Thread
import os
from scrapy.utils.project import get_project_settings
from crawler.crawler.spiders.google_scrapy import GoogleSpider
from crawler.crawler.spiders.facebook_scrapy import FacebookSpider
from crawler.crawler.spiders.instagram_scrapy import InstagramSpider

def run_spider(spider_class, nome_perfil, app_context):
    try:
        os.environ['SCRAPY_PYTHON_SHELL'] = '1'
        process = CrawlerProcess(get_project_settings())
        process.crawl(spider_class, nome_perfil=nome_perfil, app_context=app_context)
        process.start()
    except Exception as e:
        print(f"Erro no spider {spider_class.__name__}: {str(e)}")

def executar_spiders(nome_perfil, app):
    threads = []

    for spider in [FacebookSpider, InstagramSpider, GoogleSpider]:
        thread = Thread(
            target=run_spider,
            args=(spider, nome_perfil, app.app_context),
            daemon=True
        )
    
    threads.append(thread)
    thread.start()
    
    for thread in threads:
        thread.join(timeout=1800)  