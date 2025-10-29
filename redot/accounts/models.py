from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

class User(AbstractUser):
    TIPO_CHOICES = [
        ('F', 'Física'),
        ('J', 'Jurídica'),
    ]

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='F')
    rg = models.CharField(max_length=10, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    n = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=20, null=True, blank=True)
    razao_social = models.CharField(max_length=60, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    nome_usuario = models.CharField(max_length=60, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    id_role = models.IntegerField(default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'tipo': self.tipo,
            'rg': self.rg,
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
            return f"{self.nome_usuario or self.username} ({self.email})"
        else:
            return f"{self.razao_social} ({self.email})"

class Conta(models.Model):
    class Meta:
        db_table = 'conta'

    id_conta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        null=True,
        blank=True,
    )
    login = models.CharField(max_length=30, unique=True)
    senha = models.CharField(max_length=128, null=True, blank=True)
    data_criacao = models.DateField()

    def set_senha(self, raw_password):
        self.senha = make_password(raw_password)

    def check_senha(self, raw_password):
        if not self.senha:
            return False
        return check_password(raw_password, self.senha)

    def __str__(self):
        return f"Conta {self.id_conta} - {self.login}"

    def to_dict(self):
        return {
            'id_conta': self.id_conta,
            'id_usuario': self.id_usuario_id,
            'login': self.login,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }
