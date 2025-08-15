from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
from datetime import datetime
import threading
import logging
from crawler.crawler.run_crawler import executar_spiders

logging.basicConfig()
logger = logging.getLogger('apscheduler')
logger.setLevel(logging.INFO)

scrapy_lock = threading.Lock()

ultimos_resultados = {
    'dados': None,
    'ultima_execucao': None,
    'status': 'Aguardando primeira execução'
}

pesquisa_atual = {"nome_perfil": None}

def start_scrapy(frequencia, app):
    nome_perfil = pesquisa_atual.get("nome_perfil")
    if not nome_perfil:
        logger.warning(f"[{frequencia.upper()}] Nenhum perfil definido para pesquisa.")
        return
    
    with scrapy_lock:
        try:
            logger.info(f"Iniciando scraping para {nome_perfil} ({frequencia})...")
            executar_spiders(nome_perfil, app)
            
            ultimos_resultados.update({
                'dados': "Scraping concluído com sucesso",
                'ultima_execucao': datetime.now().isoformat(),
                'status': 'Sucesso'
            })
            logger.info("Scraping finalizado com sucesso!")
            
        except Exception as e:
            ultimos_resultados.update({
                'dados': None,
                'ultima_execucao': datetime.now().isoformat(),
                'status': f'Erro: {str(e)}'
            })
            logger.error(f"Falha no scraping: {str(e)}")

def start_crawler(app):
    scheduler = BackgroundScheduler(
        job_defaults={
            'max_instances': 1,
            'misfire_grace_time': 300  
        },
        timezone='America/Sao_Paulo'
    )

    jobs = [
        {
            'func': lambda: start_scrapy("minutalmente", app),
            'trigger': CronTrigger.from_crontab("* * * * *"),
            'name': "crawl_minuto"
        },
        {
            'func': lambda: start_scrapy("diariamente", app),
            'trigger': CronTrigger.from_crontab("0 0 * * *"),
            'name': "crawl_diario"
        },
        {
            'func': lambda: start_scrapy("semanalmente", app),
            'trigger': CronTrigger.from_crontab("0 0 * * MON"),
            'name': "crawl_semanal"
        },
        {
            'func': lambda: start_scrapy("mensalmente", app),
            'trigger': CronTrigger.from_crontab("0 2 1 * *"),
            'name': "crawl_mensal"
        }
    ]

    for job in jobs:
        scheduler.add_job(**job)

    try:
        scheduler.start()
        logger.info("🟢 Agendador CRON iniciado com sucesso")
        atexit.register(lambda: scheduler.shutdown())
    except Exception as e:
        logger.error(f"🔴 Falha ao iniciar agendador: {str(e)}")

def obter_resultados():
    return ultimos_resultados