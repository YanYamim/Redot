from . import db

class Conta(db.Model):
    __tablename__ = 'conta'
    
    id_conta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_cliente'))
    login = db.Column(db.String(30), unique=True)
    senha = db.Column(db.String(60), nullable=False)  
    data_criacao = db.Column(db.Date)
