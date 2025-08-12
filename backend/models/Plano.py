from . import db

class Plano(db.Model):
    __tablename__ = 'plano'
    
    id_plano = db.Column(db.Integer, primary_key=True)
    id_tipo_plano = db.Column(db.Integer, db.ForeignKey('tipo_plano.id_tipo_plano'))
    id_conta = db.Column(db.Integer, db.ForeignKey('conta.id_conta'))
    data_inicio_plano = db.Column(db.Date)
    data_fim_plano = db.Column(db.Date)
    ativa = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id_plano': self.id_plano,
            'id_tipo_plano': self.id_tipo_plano,
            'id_conta': self.id_conta,
            'data_inicio': self.data_inicio_plano,
            'data_fim': self.data_fim_plano,
            'ativa': self.ativa
        }