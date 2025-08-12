from . import db

class Tipo_Plano(db.Model):
    __tablename__ = 'tipo_plano'
    
    id_tipo_plano = db.Column(db.Integer, primary_key=True)
    nome_tipo_plano = db.Column(db.String(40))
    preco = db.Column(db.Numeric(10, 2))
    duracao_dias = db.Column(db.Integer)
    
    # Relacionamento
    planos = db.relationship('Plano', backref='tipo_plano_ref')

    def to_dict(self):
        return {
            'id_tipo_plano': self.id_tipo_plano,
            'nome': self.nome_tipo_plano,
            'preco': self.preco,
            'duracao_dias': self.duracao_dias,
        }