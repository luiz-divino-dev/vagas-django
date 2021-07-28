from django.db import models


# Create your models here.


class Experiencia(models.Model):
    curriculum = models.ForeignKey('Curriculum', on_delete=models.CASCADE)
    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100)
    tempo = models.PositiveIntegerField()
