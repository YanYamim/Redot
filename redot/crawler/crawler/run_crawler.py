import sys
import os
import django
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Configuração Django
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redot.redot.settings')

try:
    django.setup()
except Exception as e:
    print(f"Erro ao configurar Django: {e}")
    sys.exit(1)

def executar_todos_spiders(nome_perfil):
    """
    Executa todos os spiders em sequência no mesmo processo
    """
    try:
        # Usa settings do Scrapy
        settings = get_project_settings()
        settings.update({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'ROBOTSTXT_OBEY': False,
            'LOG_LEVEL': 'INFO',
            'DOWNLOAD_DELAY': 2,
            'CONCURRENT_REQUESTS': 1,
        })
        
        process = CrawlerProcess(settings)
        
        # Executa todos os spiders
        from ..crawler.spiders.facebook_scrapy import FacebookSpider
        from ..crawler.spiders.instagram_scrapy import InstagramSpider  
        from ..crawler.spiders.google_scrapy import GoogleSpider
        
        process.crawl(FacebookSpider, nome_perfil=nome_perfil)
        process.crawl(InstagramSpider, nome_perfil=nome_perfil)
        process.crawl(GoogleSpider, nome_perfil=nome_perfil)
        
        process.start()  # Bloqueia até todos terminarem
        
        return {"status": "completed", "spiders": 3}
        
    except Exception as e:
        print(f"Erro ao executar spiders: {e}")
        return {"status": "error", "error": str(e)}

def executar_spider_unico(nome_spider, nome_perfil):
    """
    Executa um spider específico
    """
    try:
        settings = get_project_settings()
        settings.update({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'ROBOTSTXT_OBEY': False,
            'LOG_LEVEL': 'INFO',
            'DOWNLOAD_DELAY': 2,
            'CONCURRENT_REQUESTS': 1,
        })
        
        process = CrawlerProcess(settings)
        
        if nome_spider == 'facebook':
            from ..crawler.spiders.facebook_scrapy import FacebookSpider
            process.crawl(FacebookSpider, nome_perfil=nome_perfil)
        elif nome_spider == 'instagram':
            from ..crawler.spiders.instagram_scrapy import InstagramSpider
            process.crawl(InstagramSpider, nome_perfil=nome_perfil)
        elif nome_spider == 'google':
            from ..crawler.spiders.google_scrapy import GoogleSpider
            process.crawl(GoogleSpider, nome_perfil=nome_perfil)
        else:
            raise ValueError(f"Spider desconhecido: {nome_spider}")
        
        process.start()
        return {"status": "completed", "spider": nome_spider}
        
    except Exception as e:
        print(f"Erro ao executar spider {nome_spider}: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--spider', help='Nome do spider (facebook|instagram|google)')
    parser.add_argument('nome_perfil', help='Nome do perfil a pesquisar')
    
    args = parser.parse_args()
    
    if args.spider:
        resultado = executar_spider_unico(args.spider, args.nome_perfil)
    else:
        resultado = executar_todos_spiders(args.nome_perfil)
    
    print(f"Resultado: {resultado}")