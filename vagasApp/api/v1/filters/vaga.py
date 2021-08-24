import django_filters as filters

from vagasApp.models import Vaga, Candidato
from datetime import datetime

class VagaFilter(filters.FilterSet):
    empresa = filters.CharFilter(field_name='empresa', lookup_expr='icontains')
    candidato_apply = filters.CharFilter(method='filter_candidato_apply')


    class Meta:
        model = Vaga
        fields = ['empresa', 'cargo', 'candidato_apply']


    def filter_candidato_apply(self,queryset, name, value):
        return queryset.filter(candidato_apply__nome_candidato=value)


class CandidatoFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    data_inicio = filters.CharFilter(method='filter_data_inicio', label='data de inicio')
    data_fim = filters.CharFilter(method='filter_data_fim', label='data fim')
    email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Candidato
        fields = ['status', 'data_inicio', 'data_fim', "email"]

    def filter_data_inicio(self, queryset, name, value):
        try:
            date_time = datetime.strptime(value, '%d/%m/%Y')
        except Exception:
            return queryset
        return queryset.filter(data_nascimento__gte=date_time)

    def filter_data_fim(self, queryset, name, value):
        try:
            date_time = datetime.strptime(value, '%d/%m/%Y')
        except Exception:
            return queryset
        return queryset.filter(data_nascimento__lte=date_time)
