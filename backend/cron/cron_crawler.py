from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
from crawler.crawler.run_crawler import executar_spiders 
from datetime import datetime

ultimos_resultados = {
    'dados': None,
    'ultima_execucao': None,
    'status': 'Aguardando primeira execução'
}

pesquisa_atual = {"nome_perfil": None}

def start_scrapy(frequencia, app):
    nome_perfil = pesquisa_atual.get("nome_perfil")
    if not nome_perfil:
        print(f"[{frequencia.upper()}] Nenhum termo para pesquisar ainda.")
        return
    
    try:
        resultados = executar_spiders(nome_perfil, app)
        ultimos_resultados['dados'] = resultados
        ultimos_resultados['ultima_execucao'] = datetime.now().isoformat()
        ultimos_resultados['status'] = 'Sucesso'
        print("Pesquisa concluída com sucesso!")
    except Exception as e:
        ultimos_resultados['status'] = f'Erro: {str(e)}'
        print(f"Erro na pesquisa: {e}")

def start_crawler(app):
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        lambda: start_scrapy("minutalmente", app),
        CronTrigger.from_crontab("* * * * *"),
        name="crawl_minutal"
    )

    scheduler.add_job(
        lambda: start_scrapy("diariamente", app),
        CronTrigger.from_crontab("0 0 * * *"),
        name="crawl_diario"
    )

    scheduler.add_job(
        lambda: start_scrapy("semanalmente", app),
        CronTrigger.from_crontab("0 0 * * MON"),
        name="crawl_semanal"
    )

    scheduler.add_job(
        lambda: start_scrapy("mensalmente", app),
        CronTrigger.from_crontab("0 2 1 * *"),
        name="crawl_mensal"
    )

    scheduler.start()
    print("[CRON] Agendador iniciado.")
    atexit.register(lambda: scheduler.shutdown())

def obter_resultados():
    return ultimos_resultados