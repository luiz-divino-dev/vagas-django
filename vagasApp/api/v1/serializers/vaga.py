from rest_framework import serializers
from vagasApp.models import Vaga, Candidato


class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = '__all__'


class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = '__all__'

    # def to_representation(self, instance):
    #     payload = super(CandidatoSerializer, self).to_representation(instance)
    #     action = self.context.get('view').action
    #     if action == 'list':
    #         payload.pop('nome_candidato', None)
    #     return payload