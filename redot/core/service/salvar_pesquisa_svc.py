from ..models import Pesquisa
import traceback
import threading

def salvar_pesquisa(data):
    """
    Salva os resultados da pesquisa no banco de dados
    """
    try:
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

def salvar_pesquisa_thread(data):
    """Salva dados em uma thread separada para evitar problemas de async"""
    def save():
        try:
            resultado_valor = data.get('resultado') or data.get('nome_resultado')
            
            nova_pesquisa = Pesquisa(
                nome_pesquisa=data['nome_pesquisa'],
                resultado=resultado_valor,
                fonte=data['fonte'],
                url_resultado=data['url']
            )

            nova_pesquisa.save()
            print(f"Dados salvos em thread! ID: {nova_pesquisa.id_pesquisa}")
            return nova_pesquisa.to_dict(), 200
            
        except Exception as e:
            print(f"Erro ao salvar em thread: {e}")
            return {'error': str(e)}, 500
    
    thread = threading.Thread(target=save)
    thread.daemon = True
    thread.start()
    return {"status": "started"}, 200

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