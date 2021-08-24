from functools import wraps

from django.views.decorators.http import require_http_methods
from django.db.models.functions.datetime import datetime
from django.http import HttpResponse


from datetime import datetime
# request.
from rest_framework.exceptions import ValidationError


def future_date(date_list):
    def decorator(func):
        @wraps(func)
        def inner(self, request, *args, **kwargs):
            erros =[]
            for date in date_list:
                data_nascimento = request.data.get(date)
                data_nascimento  = datetime.strptime(data_nascimento, '%Y-%m-%d')
                data_atual = datetime.now()
                if data_nascimento > data_atual:
                    erros.append(f"Data {date} não pode ser futura!")

            if erros:
                raise ValidationError({"erros": erros})

            return func(self, request, *args, **kwargs)

        return inner
    return decorator


