from flask import jsonify, request
from crawler.crawler.run_crawler import executar_spiders
from cron.cron_crawler import pesquisa_atual
from services.salvar_pesquisa_service import buscar_resultados_bd

def rotas_cron(app):
    @app.route('/radar', methods=['POST'])
    def rota_crawler():
        data = request.get_json()
        nome_perfil = data.get('nome_perfil')

        if not nome_perfil:
            return jsonify({"erro": "nome_perfil é obrigatório"}), 400
        
        pesquisa_atual["nome_perfil"] = nome_perfil

        executar_spiders(nome_perfil, app)
        return jsonify({"mensagem": f"Spiders executadas para o perfil '{nome_perfil}'"}), 200
    
    @app.route('/radar/resultados', methods=['POST'])
    def obter_resultados():
        data = request.get_json()
        nome_perfil = data.get('nome_perfil')
        
        if not nome_perfil:
            return jsonify({"erro": "Parâmetro 'nome_perfil' é obrigatório"}), 400
        
        try:
            resultados = buscar_resultados_bd(nome_perfil)
            return jsonify(resultados)
            
        except Exception as e:
            return jsonify({
                "erro": str(e),
                "resultados": [],
                "total": 0,
                "status": "erro"
            }), 500
    
    @app.route('/radar/status', methods=['GET'])
    def status_cron():
        return jsonify(obter_resultados())
    