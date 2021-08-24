# from ..views.vaga import CurriculimViewSet
from vagasApp.models import Curriculum
from rest_framework import serializers


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'

