from django.db import models


class Vagas(models.Model):
    empresa = models.CharField(max_length=50, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    vagas_ofertadas = models.PositiveSmallIntegerField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

