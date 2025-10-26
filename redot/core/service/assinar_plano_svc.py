from datetime import date, timedelta
from django.db import transaction
from ..models import Plano, TipoPlano
import traceback

def assinar_plano(data):
    try:
        with transaction.atomic():
            if not data.get("id_tipo_plano") or not data.get("id_conta"):
                return {"error": "id_tipo_plano e id_conta são obrigatórios"}, 400
            
            try:
                tipo_plano = TipoPlano.objects.get(id_tipo_plano=data['id_tipo_plano'])
            except TipoPlano.DoesNotExist:
                return {"error": "Tipo de plano não encontrado"}, 404

            data_inicio_plano = date.today()
            data_fim_plano = data_inicio_plano + timedelta(days=tipo_plano.duracao_dias)

            nova_assinatura = Plano(
                id_tipo_plano=tipo_plano,
                id_conta_id=data['id_conta'],
                data_inicio_plano=data_inicio_plano,
                data_fim_plano=data_fim_plano,
                ativa=True
            )

            data_expiracao = data_inicio_plano + timedelta(days=tipo_plano.duracao_dias)

            if date.today() > data_expiracao:
                nova_assinatura.ativa = False

            nova_assinatura.save()

            return nova_assinatura.to_dict(), 200
    
    except Exception:
        print("Erro ao assinar plano:", traceback.format_exc())
        return {"error": "Erro interno do servidor"}, 500