from django.db import models


class Cep(models.Model):
    cidade = models.CharField(max_length=50, db_index=True, default='Guarabira')
    cep = models.CharField(max_length=9, unique=True)
    logradouro = models.CharField(max_length=150, db_index=True)
    bairro = models.CharField(max_length=100, db_index=True)
    tipo_codificacao = models.CharField(max_length=100, null=True, blank=True)
    numero_inicial = models.CharField(max_length=15, null=True, blank=True)
    numero_final = models.CharField(max_length=15, null=True, blank=True)
    trecho = models.CharField(max_length=15, null=True, blank=True)
    lado = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f'{self.cep} - {self.logradouro}'
