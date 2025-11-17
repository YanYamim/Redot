import sys
import os
import threading
import subprocess
import argparse
import django
from django.conf import settings
        
from ..crawler.spiders.facebook_scrapy import FacebookSpider
from ..crawler.spiders.instagram_scrapy import InstagramSpider  
from ..crawler.spiders.google_scrapy import GoogleSpider
from scrapy.crawler import CrawlerProcess
from scrapy import signals

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redot.redot.settings')

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
    def _run_sequence(profile_name):
        spiders = ['facebook', 'instagram', 'google']
        script = os.path.abspath(__file__)
        py = sys.executable or 'python'

        for sp in spiders:
            try:
                cmd = [py, script, '--single-spider', sp, profile_name]
                subprocess.run(cmd)
            except Exception as e:
                print(f"[run_crawler] error running spider {sp}: {e}")

    try:
        
        t = threading.Thread(target=_run_sequence, args=(nome_perfil,), daemon=True)
        t.start()
        return {"status": "started", "spiders": 3}
   
    except Exception as e:
        print(f"Erro ao iniciar execução das spiders: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--single-spider', help='Run a single spider by name (facebook|instagram|google)')
    parser.add_argument('nome_perfil', nargs='?', default='mavip')
    args = parser.parse_args()

    if args.single_spider:
        spider_name = args.single_spider.lower()
        nome = args.nome_perfil

        settings = {
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'ROBOTSTXT_OBEY': False,
            'LOG_LEVEL': 'INFO',
            'DOWNLOAD_DELAY': 2,
            'CONCURRENT_REQUESTS': 1,
        }

        process = CrawlerProcess(settings)

        if spider_name == 'facebook':
            process.crawl(FacebookSpider, nome_perfil=nome)
        elif spider_name == 'instagram':
            process.crawl(InstagramSpider, nome_perfil=nome)
        elif spider_name == 'google':
            process.crawl(GoogleSpider, nome_perfil=nome)
        else:
            print(f"Unknown spider: {spider_name}")
            sys.exit(2)

        # capture spider finish reason via Scrapy signals so we can propagate
        # an appropriate exit code to the caller when running in subprocess
        finish = {'reason': None}

        def _spider_closed(spider, reason):
            try:
                # reason is a str describing why the spider finished
                finish['reason'] = reason
                print(f"[run_crawler] spider_closed signal received: reason={reason}")
            except Exception:
                finish['reason'] = 'unknown'

        process.signals.connect(_spider_closed, signal=signals.spider_closed)

        process.start()
        print(f"[run_crawler] single-spider mode: finished '{spider_name}' for perfil='{nome}'")

        # map finish reason to exit codes so a subprocess caller can detect failures
        reason = finish.get('reason')
        if reason:
            # CloseSpider('Perfil não encontrado') will surface as that exact string
            if 'Perfil não encontrado' in reason:
                print(f"[run_crawler] exiting with code 3 due to reason: {reason}")
                sys.exit(3)
            elif reason != 'finished':
                print(f"[run_crawler] exiting with code 4 due to non-finished reason: {reason}")
                sys.exit(4)
        # normal success
        sys.exit(0)
    else:
        resultado = executar_spiders(args.nome_perfil)
