from datetime import date
from models import db, Conta
import traceback

def cadastrar_conta(usuario, data):
    try:
        nova_conta = Conta(
            id_usuario=usuario.id_usuario,
            login=data['email'],
            senha=data['senha'],
            data_criacao=date.today()
        )

        db.session.add(nova_conta)
        db.session.commit()

        return nova_conta
    except Exception as e:
        db.session.rollback()
        print("Erro ao cadastrar conta:", traceback.format_exc())
        return None