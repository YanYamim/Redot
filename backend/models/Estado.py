from . import db

class Estado(db.Model):
    __tablename__ = 'estado'

    id_estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_estado = db.Column(db.String(45))
    sigla_estado = db.Column(db.String(2))

    def to_dict(self):
        return {
            'id_estado': self.id_estado,
            'nome_estado': self.nome_estado,
            'sigla_estado': self.sigla_estado,
        }