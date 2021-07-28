from django.db import models


class Curriculum(models.Model):
    nome_curriculum = models.CharField(max_length=100, blank=True, null=True)
    area_formacao = models.CharField(max_length=100, blank=True, null=True)
    grau_de_instrucao = models.CharField(max_length=50, blank=True, null=True)
    candidato = models.OneToOneField('Candidato', on_delete=models.CASCADE, null=True, blank=True)
