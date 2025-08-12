from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .Conta import Conta
from .Pesquisa import Pesquisa
from .Usuario import Usuario
from .Estado import Estado
from .Plano import Plano
from .Tipo_plano import Tipo_Plano

# Opcional: para facilitar imports
__all__ = ['Conta', 'Pesquisa', 'Usuario', 'Estado', 'Plano', 'Tipo_Plano']
