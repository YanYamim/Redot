from django.db import transaction
from models import Pesquisa
import traceback

def salvar_pesquisa(data):
    """
    Salva os resultados da pesquisa no banco de dados
    """
    try:
        with transaction.atomic():
            resultado_valor = data.get('resultado') or data.get('nome_resultado')
            
            nova_pesquisa = Pesquisa(
                nome_pesquisa=data['nome_pesquisa'],
                resultado=resultado_valor,
                fonte=data['fonte'],
                url_resultado=data['url']
            )

            nova_pesquisa.save()
            return nova_pesquisa.to_dict(), 200

    except Exception as e:
        print("Erro ao salvar a pesquisa:", traceback.format_exc())
        return {'error': str(e)}, 500

def buscar_resultados_bd(nome_perfil):
    try:
        resultados = Pesquisa.objects.filter(
            nome_pesquisa=nome_perfil
        ).order_by(
            '-id_pesquisa'
        ).all()
        
        return {
            "resultados": [{
                "titulo": r.resultado,
                "fonte": r.fonte.lower(),  
                "url": r.url_resultado,
                "id": r.id_pesquisa
            } for r in resultados],
            "total": len(resultados),
            "status": "completo"
        }
        
    except Exception as e:
        print("Erro ao buscar resultados:", traceback.format_exc())
        raise e