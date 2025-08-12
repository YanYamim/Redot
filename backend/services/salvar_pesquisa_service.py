from models import db, Pesquisa
import traceback
from flask import jsonify

def salvar_pesquisa(data):
    try:
        nova_pesquisa = Pesquisa(
            nome_pesquisa=data['nome_pesquisa'],
            nome_resultado=data['nome_resultado'],
            fonte=data['fonte'],
            url_resultado=data['url']
        )

        db.session.add(nova_pesquisa)
        db.session.commit()

        return nova_pesquisa.to_dict(), 200

    except Exception as e:
        db.session.rollback()
        print("Erro ao salvar a pesquisa:", traceback.format_exc())
        return {'error': str(e)}, 500
    
def buscar_resultados_bd(nome_perfil):
    try:
        resultados = Pesquisa.query.filter_by(
            nome_pesquisa=nome_perfil
        ).order_by(
            Pesquisa.id_pesquisa.desc()
        ).all()
        
        return {
            "resultados": [{
                "titulo": r.nome_resultado,
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