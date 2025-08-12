from flask import request
from services.assinar_plano_service import assinar_plano
from flask import jsonify

def rotas_assinatura(app):
    @app.post('/planos/pagamento')
    def plano_assinado():
        print("Dados recebidos:", request.json)
        data = request.get_json()
        response, status_code = assinar_plano(data)
        return jsonify(response), status_code