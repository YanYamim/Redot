from datetime import date, timedelta
from models import db, Plano, Tipo_Plano
import traceback

def assinar_plano(data):
    try:

        if not data.get("id_tipo_plano") or not data.get("id_conta"):
            db.session.rollback()
            return None, 500
        
        tipo_plano = Tipo_Plano.query.get(data['id_tipo_plano'])
        
        data_inicio_plano = date.today()
        data_fim_plano = data_inicio_plano + timedelta(days=tipo_plano.duracao_dias)

        nova_assinatura = Plano(
            id_tipo_plano=tipo_plano.id_tipo_plano,
            id_conta=data['id_conta'],
            data_inicio_plano=data_inicio_plano,
            data_fim_plano=data_fim_plano,
            ativa=True
        )

        data_expiracao = data_inicio_plano + timedelta(days=tipo_plano.duracao_dias)

        if date.today() > data_expiracao:
            nova_assinatura.ativa = False

        db.session.add(nova_assinatura)
        db.session.commit()

        return nova_assinatura.to_dict(), 200
    
    except Exception as e:
        db.session.rollback()
        print("Erro ao cadastrar conta:", traceback.format_exc())
        return None, 500
