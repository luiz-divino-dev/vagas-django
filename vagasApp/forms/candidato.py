from django import forms
from vagasApp.models import Candidato, Vagas, Curriculum
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# ctrl+ shift mover linha
# form de registro User
class UserForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user


class CandidatoFormRegister(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['nome_candidato', 'email', 'phone', 'user']


class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['area_formacao', 'nome_curriculum', 'grau_de_instrucao']


class CurriculumRegisterForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['area_formacao', 'nome_curriculum', 'grau_de_instrucao', 'candidato']


class VagasForm(forms.ModelForm):
    class Meta:
        model = Vagas
        fields = ['empresa', 'cargo', 'descricao']


# class CandidatoFormLogin(forms.ModelForm):
#     class Meta:
#         model = Candidato
#         fields = ['usuario', 'senha']
