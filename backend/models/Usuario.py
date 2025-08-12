from . import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(1))  
    rg = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    cep = db.Column(db.String(8))
    n = db.Column(db.Integer)  
    complemento = db.Column(db.String(20))
    razao_social = db.Column(db.String(60))
    cnpj = db.Column(db.String(14), unique=True)
    nome_usuario = db.Column(db.String(60))
    cpf = db.Column(db.String(11), unique=True)

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'tipo': self.tipo,
            'rg': self.rg,
            'email': self.email,
            'telefone': self.telefone,
            'celular': self.celular,
            'cep': self.cep,
            'n': self.n,
            'complemento': self.complemento,
            'razao_social': self.razao_social,
            'cnpj': self.cnpj,
            'nome_usuario': self.nome_usuario,
            'cpf': self.cpf
        }
