from django.urls import path, include

from rest_framework_nested import routers
from vagasApp.api.v1 import views

router = routers.DefaultRouter()

router.register('vaga', views.VagaViewSet, basename='vaga')
router.register('candidato', views.CandidatoViewSet, basename='candidato')
router.register('curriculim', views.CurriculimViewSet, basename='curriculum')

urlpatterns = [
    path('', include(router.urls))
]
