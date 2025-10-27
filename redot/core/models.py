from django.db import models
from ..accounts.models import Conta

class Estado(models.Model):
    class Meta:
        db_table = 'estado'

    id_estado = models.AutoField(primary_key=True)
    nome_estado = models.CharField(max_length=45)
    sigla_estado = models.CharField(max_length=2)

    def to_dict(self):
        return {
            'id_estado': self.id_estado,
            'nome_estado': self.nome_estado,
            'sigla_estado': self.sigla_estado,
        }

    def __str__(self):
        return f"{self.nome_estado} ({self.sigla_estado})"

class TipoPlano(models.Model):
    class Meta:
        db_table = 'tipo_plano'

    id_tipo_plano = models.AutoField(primary_key=True)
    nome_tipo_plano = models.CharField(max_length=40)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao_dias = models.IntegerField()

    def to_dict(self):
        return {
            'id_tipo_plano': self.id_tipo_plano,
            'nome': self.nome_tipo_plano,
            'preco': float(self.preco) if self.preco else None,
            'duracao_dias': self.duracao_dias,
        }

    def __str__(self):
        return f"{self.nome_tipo_plano} - {self.preco}"


class Plano(models.Model):
    class Meta:
        db_table = 'plano'

    id_plano = models.AutoField(primary_key=True)
    id_tipo_plano = models.ForeignKey(TipoPlano, on_delete=models.CASCADE, db_column='id_tipo_plano')
    id_conta = models.ForeignKey(Conta, on_delete=models.CASCADE, db_column='id_conta')
    data_inicio_plano = models.DateField()
    data_fim_plano = models.DateField()
    ativa = models.BooleanField(default=True)
    
    def to_dict(self):
        return {
            'id_plano': self.id_plano,
            'id_tipo_plano': self.id_tipo_plano.id_tipo_plano,
            'id_conta': self.id_conta.id_conta,
            'data_inicio': self.data_inicio_plano.isoformat() if self.data_inicio_plano else None,
            'data_fim': self.data_fim_plano.isoformat() if self.data_fim_plano else None,
            'ativa': self.ativa
        }

    def __str__(self):
        return f"Plano {self.id_plano} - Conta {self.id_conta.id_conta}"


class Pesquisa(models.Model):
    class Meta:
        db_table = 'pesquisa'
    
    id_pesquisa = models.AutoField(primary_key=True)
    nome_pesquisa = models.CharField(max_length=50)
    resultado = models.CharField(max_length=100)
    fonte = models.CharField(max_length=50)
    url_resultado = models.CharField(max_length=255)

    def to_dict(self):
        return {
            'id_pesquisa': self.id_pesquisa,
            'nome_pesquisa': self.nome_pesquisa,
            'resultado': self.resultado,
            'fonte': self.fonte,
            'url_resultado': self.url_resultado
        }

    def __str__(self):
        return f"{self.nome_pesquisa} - {self.resultado}"