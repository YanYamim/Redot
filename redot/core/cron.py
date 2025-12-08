import threading
import logging
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

logger = logging.getLogger('cron')
scrapy_lock = threading.Lock()

ultimos_resultados = {
    'dados': None,
    'ultima_execucao': None,
    'status': 'Aguardando primeira execução'
}

pesquisa_atual = {"nome_perfil": None}

def start_scrapy(frequencia):
    """
    Função para executar o scraping baseado na frequência
    """
    nome_perfil = pesquisa_atual.get("nome_perfil")
    if not nome_perfil:
        logger.warning(f"[{frequencia.upper()}] Nenhum perfil definido para pesquisa.")
        return
    
    with scrapy_lock:
        try:
            logger.info(f"Iniciando scraping para {nome_perfil} ({frequencia})...")
            
            # Executa spiders direto sem run_crawler.py
            settings = get_project_settings()
            process = CrawlerProcess(settings)
            process.crawl('instagram', nome_perfil=nome_perfil)
            process.crawl('google', nome_perfil=nome_perfil)
            process.crawl('facebook', nome_perfil=nome_perfil)
            process.start()
            
            ultimos_resultados.update({
                'dados': {'status': 'completo'},
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
            logger.exception("Falha no scraping")

def crawl_minutalmente():
    """Executa a cada minuto"""
    start_scrapy("minutalmente")

def crawl_diariamente():
    """Executa diariamente à meia-noite"""
    start_scrapy("diariamente")

def crawl_semanalmente():
    """Executa semanalmente às segundas-feiras à meia-noite"""
    start_scrapy("semanalmente")

def crawl_mensalmente():
    """Executa mensalmente no primeiro dia do mês às 02:00"""
    start_scrapy("mensalmente")

def obter_resultados():
    """Função para obter os últimos resultados"""
    return ultimos_resultados

def definir_perfil_pesquisa(nome_perfil):
    """
    Função para definir o perfil a ser pesquisado
    Pode ser chamada a partir das views
    """
    pesquisa_atual["nome_perfil"] = nome_perfil
    logger.info(f"Perfil de pesquisa definido para: {nome_perfil}")