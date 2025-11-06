import sys
import django
from django.conf import settings
        
from crawler.spiders.facebook_scrapy import FacebookSpider
from crawler.spiders.instagram_scrapy import InstagramSpider  
from crawler.spiders.google_scrapy import GoogleSpider
from scrapy.crawler import CrawlerProcess

sys.path.insert(0, '/home/yanyamim/Documentos/trabalhos/python_scrappy')

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'redot',
                'USER': 'postgres',
                'PASSWORD': '1234',
                'HOST': '127.0.0.1',
                'PORT': '15432',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'redot.core',
            'redot.accounts',
        ],
        USE_TZ=True,
        SECRET_KEY='django-insecure-temp-key-for-crawler',
    )

try:
    django.setup()
        
except Exception as e:
    print(f"Erro ao configurar Django: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def executar_spiders(nome_perfil):
    """
    Função principal para executar todos os spiders
    """    
    try:
        
        crawler_path = '/home/yanyamim/Documentos/trabalhos/python_scrappy/redot/crawler'
        if crawler_path not in sys.path:
            sys.path.insert(0, crawler_path)
                
        settings = {
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'ROBOTSTXT_OBEY': False,
            'LOG_LEVEL': 'INFO',
            'DOWNLOAD_DELAY': 2,
            'CONCURRENT_REQUESTS': 1,
        }
        
        process = CrawlerProcess(settings)
        
        process.crawl(FacebookSpider, nome_perfil=nome_perfil)
        process.crawl(InstagramSpider, nome_perfil=nome_perfil) 
        process.crawl(GoogleSpider, nome_perfil=nome_perfil)
        
        process.start()
        
        return {"status": "completed", "spiders": 3}
        
    except Exception as e:
        print(f"Erro ao executar spiders: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    resultado = executar_spiders("mavip")
    print(f"Resultado: {resultado}")