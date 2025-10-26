"""
Configuração do pytest para os testes Django
"""
import pytest
import os
import sys
import django
from pathlib import Path

# Adiciona o diretório raiz ao Python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redot.redot.settings')

def pytest_configure(config):
    """Configura o Django antes de rodar os testes"""
    django.setup()

@pytest.fixture(scope='session')
def django_db_setup():
    """Configuração do banco de dados para testes"""
    pass
