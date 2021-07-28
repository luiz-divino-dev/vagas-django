from django.db import models
from django.contrib.auth.models import User


class Candidato(models.Model):
    nome_candidato = models.CharField(max_length=100)
    phone = models.PositiveIntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # remover
    email = models.EmailField(max_length=255, blank=True)

    def __str__(self):
        return str(self.nome_candidato)
