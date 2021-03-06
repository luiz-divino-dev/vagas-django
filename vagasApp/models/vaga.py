from django.db import models


class Vaga(models.Model):
    empresa = models.CharField(max_length=50, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    candidato_aceito = models.OneToOneField('Candidato', on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='aceito')
    status = models.CharField(max_length=1, blank=True, null=True, default='D')
    candidato_apply = models.ManyToManyField('Candidato', blank=True)
    # status : O 'ocupado', D 'disponível'

    class Meta:
        pass
        # db_table = 'vagas'
        # verbose_name = 'Vaga'
        # verbose_name_plural = 'Vagas'

        # unique_together =['empresa', 'candidato_apply']
