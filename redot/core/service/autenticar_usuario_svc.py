def login_usuario(email, senha):
    USUARIO_FIXO = {
        "email": "mavip@teste.com",
        "senha": "123"
    }

    if not email or not senha:
        return {"status": "error", "message": "Email e senha são obrigatórios"}, 400
    
    if email == USUARIO_FIXO["email"] and senha == USUARIO_FIXO["senha"]:
        return {"status": "success", "message": "Autenticação bem-sucedida"}, 200
    else:
        return {"status": "error", "message": "Credenciais inválidas"}, 401