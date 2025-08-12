from flask import request
from services.cadastrar_usuario_service import cadastrar_usuario

def rotas_usuario(app):
    @app.route('/usuario/cadastro', methods=['POST'])
    def novo_usuario():
        data = request.get_json()
        response, status_code = cadastrar_usuario(data)
        return response, status_code