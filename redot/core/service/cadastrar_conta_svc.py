from datetime import date
from django.db import transaction
from ..models import Conta
import traceback

def cadastrar_conta(usuario, data):
    try:
        with transaction.atomic():
            nova_conta = Conta(
                id_usuario=usuario,
                login=data['email'],
                senha=data['senha'],
                data_criacao=date.today()
            )

            nova_conta.save()

            return nova_conta
    except Exception:
        print("Erro ao cadastrar conta:", traceback.format_exc())
        return None