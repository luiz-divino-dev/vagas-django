from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.date_decorator import future_date
from vagasApp.api.v1.filters import VagaFilter, CandidatoFilter
from vagasApp.api.v1.serializers import VagaSerializer, CandidatoSerializer, CurriculumSerializer
from vagasApp.models import Vaga, Candidato, Curriculum


class VagaViewSet(viewsets.ModelViewSet):
    serializer_class = VagaSerializer
    queryset = Vaga.objects.all()
    filter_class = VagaFilter
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        empresa = request.data
        vaga_serializer = VagaSerializer(data=request.data)
        vaga_serializer.is_valid(raise_exception=True)
        vaga = vaga_serializer.save()
        return Response(vaga_serializer.data)


class CandidatoViewSet(viewsets.ModelViewSet):
    serializer_class = CandidatoSerializer
    # queryset = Candidato.objects.all()
    filter_class = CandidatoFilter

    def get_queryset(self):
        usuario = self.request.user
        queryset = Candidato.objects.filter(user=usuario.id)
        return queryset

    @future_date(['data_nascimento', ])
    def create(self, request, *args, **kwargs):
        return super(CandidatoViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        usuario = self.request.user
        candidato = Candidato.objects.get(user=usuario.id)
        candidato_obj = self.get_queryset().defer('nome_candidato')  # da erro

        # candidato_serializer = CandidatoSerializer(self.get_queryset(), context=self.get_serializer_context(), many=True)#usar get_queryset (em vez de queryset)
        candidato_serializer = CandidatoSerializer(self.get_queryset(),
                                                   many=True)  # usar get_queryset (em vez de queryset)

        # não é precisa usar isvalid(), data() é para criar
        return Response(candidato_serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CandidatoSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CurriculimViewSet(viewsets.ModelViewSet):
    # queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        usuario = self.request.user
        queryset = Curriculum.objects.filter(candidato__user=usuario)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     serializer.is_valid()
    #     serializer.data
    #     CandidatoSerializer(instance=obj, data={"email": "google.com"}, partial=True)
    #     return Response()

    def create(self, request, *args, **kwargs):
        curriculum_serializer = CurriculumSerializer(data=request.data)
        if curriculum_serializer.is_valid():
            curriculum_serializer.save()
        return Response(curriculum_serializer.data)
