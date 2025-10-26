from django.db import models

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


class Usuario(models.Model):
    TIPO_CHOICES = [
        ('F', 'Física'),
        ('J', 'Jurídica'),
    ]

    class Meta:
        db_table = 'usuario'

    id_usuario = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    rg = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=100, unique=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    n = models.IntegerField(null=True, blank=True)  #
    complemento = models.CharField(max_length=20, null=True, blank=True)
    razao_social = models.CharField(max_length=60, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    nome_usuario = models.CharField(max_length=60, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    id_role = models.IntegerField(default=1)

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
            'cpf': self.cpf,
            'id_role': self.id_role
        }

    def __str__(self):
        if self.tipo == 'F':
            return f"{self.nome_usuario} ({self.email})"
        else:
            return f"{self.razao_social} ({self.email})"


class Conta(models.Model):
    class Meta:
        db_table = 'conta'

    id_conta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    login = models.CharField(max_length=30, unique=True)
    senha = models.CharField(max_length=60)
    data_criacao = models.DateField()

    def __str__(self):
        return f"Conta {self.id_conta} - {self.login}"

    def to_dict(self):
        return {
            'id_conta': self.id_conta,
            'id_usuario': self.id_usuario.id_usuario,
            'login': self.login,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }


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