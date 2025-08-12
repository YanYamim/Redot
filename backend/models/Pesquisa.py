from . import db

class Pesquisa(db.Model):
    __tablename__ = 'pesquisa'
    
    id_pesquisa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_pesquisa = db.Column(db.String(50))
    nome_resultado = db.Column(db.String(100))
    fonte = db.Column(db.String(50))
    url_resultado = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id_pesquisa': self.id_pesquisa,
            'nome_pesquisa': self.nome_pesquisa,
            'nome_resultado': self.nome_resultado,
            'fonte': self.fonte,
            'url_resultado': self.url_resultado
        }