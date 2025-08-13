from flask import request
from services.cadastrar_usuario_service import cadastrar_usuario
from services.autenticar_usuario_service import login_usuario

def rotas_usuario(app):
    @app.route('/usuario/cadastro', methods=['POST'])
    def novo_usuario():
        data = request.get_json()
        response, status_code = cadastrar_usuario(data)
        return response, status_code
    
    @app.post('/login')
    def autenticacao():
        data = request.get_json()
        email = data['email']
        senha = data['senha']
        response, status_code = login_usuario(email, senha)
        return response, status_code