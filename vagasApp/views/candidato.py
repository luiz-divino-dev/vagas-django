from django import views
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from vagasApp.forms import CandidatoFormRegister, UserForm, CurriculumForm, VagasForm
from vagasApp.forms.candidato import CurriculumRegisterForm
from vagasApp.models import Curriculum, Candidato, Vagas
# from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views import generic
from django.views.generic.edit import CreateView


# class


class CandidatoViewRegister(views.View):
    template_name = 'candidatoTemplate.html'

    def get(self, request):
        return render(self.request, self.template_name, {'titulo': 'Formulário de registro'})

    @transaction.atomic
    def post(self, request):
        form_candidato = CandidatoFormRegister(request.POST)
        form_user = UserForm(request.POST)
        if form_candidato.is_valid() and form_user.is_valid():
            # username = form_user.cleaned_data.get('username')
            # password = form_user.cleaned_data.get('password1')
            user = form_user.save()
            data = {
                'user': user,
                'email': form_candidato.cleaned_data.get('email'),
                'nome_candidato': form_candidato.cleaned_data.get('nome_candidato'),
                'phone': form_candidato.cleaned_data.get('phone')
            }
            form_candidato2 = CandidatoFormRegister(data)
            if form_candidato2.is_valid():
                form_candidato2.save()
            else:
                messages.error(request, 'Falha no registro')
            # user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, 'Registrado com sucesso')
            return redirect('vagas:login')
        form_user = UserForm()
        return render(self.request, self.template_name, {'titulo': 'Formulário de registro'})


class CandidatoViewLogin(views.View):
    template_name = 'candidato_login_template.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password')
        #     user = authenticate(username=username, password=password)
        #     if user is not None:
        #         login(request, user)
        #         messages.info(request, f"You are now logged in as {username}.")
        #         return redirect("vagas:homePage")
        #     else:
        #         messages.error(request, "Invalid username or password.")
        # else:
        #     messages.error(request, "Invalid username or password.")
        #
        # # form = AuthenticationForm()
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.is_superuser:
                return redirect('vagas:homePage')
            else:
                return redirect('vagas:home_super')

        else:
            messages.error(request, "Invalid username or password.")

        return render(request, self.template_name)


class TemplateHome(generic.TemplateView):
    template_name = 'Home.html'


class HomePageCandidato(views.View):
    template_name = 'HomePage.html'
    vagas = Vagas.objects.filter(status='D')

    def get(self, request):
        return render(request, self.template_name, {'vagas': self.vagas})

    def post(self, request):
        cod = request.POST['cod_vaga']
        usuario = request.user
        candidato = Candidato.objects.get(user=usuario.id)
        if candidato.status == 'O':
            messages.error(request,
                           'você não pode se candidatar, pois já está ocupando ou se candidatando para uma vaga')
            return render(request, self.template_name, {'vagas': self.vagas})
        candidato.status = 'O'
        vaga = Vagas.objects.get(id=cod)
        vaga.candidato_apply_id = candidato.id
        vaga.save()
        candidato.save()
        return redirect('vagas:login')


class CurriculumView(views.View):
    template_name = 'curriculumTemplate.html'

    def get(self, request):
        context = {}

        user = request.user

        curriculum = Curriculum.objects.filter(candidato__user=user)

        if curriculum:
            context = {
                'form_curriculo': CurriculumForm(instance=curriculum.first())
            }
        else:
            context = {
                'form_curriculo': CurriculumForm()

            }

        return render(request, self.template_name, context=context)

    @transaction.atomic
    def post(self, request):
        form_curriculum = CurriculumForm(request.POST)
        usuario = request.user
        candidato = Candidato.objects.get(user=usuario.id)

        if Curriculum.objects.filter(candidato=candidato):
            curriculum = CurriculumForm(instance=candidato.curriculum, data=request.POST, )
            curriculum.is_valid()
            curriculum.save()
            return redirect('vagas:homePage')

        if not form_curriculum.is_valid():
            messages.error(request, 'Falha no registro')

        data = {
            **form_curriculum.cleaned_data,
            'candidato': candidato
        }
        form_curriculum2 = CurriculumRegisterForm(data)
        if form_curriculum2.is_valid():
            form_curriculum2.save()
            return redirect('vagas:homePage')
        else:
            messages.error(request, 'Falha no registro')


class AceitarCandidato(views.View):
    template_name = 'aceitar_candidato.html'
    vagas = Vagas.objects.filter(candidato_apply_id__isnull=False, status='D')
    # candidatos = Candidato.objects.filter('O')
    # curriculim = Curriculum.objects.filter()

    def get(self, request):
        # usuario = request.user
        lista = []
        for vaga in self.vagas:
            lista.append(
                {
                    'vaga': vaga,
                    'curriculos': Curriculum.objects.filter(candidato__vagas=vaga)
                }
            )
        return render(request, self.template_name, {'lista': lista})

    def post(self, request):
        cod = request.POST['cod_vaga']
        nome = request.POST['nome_candidato']
        candidato = Candidato.objects.get(nome_candidato=nome)
        vaga = Vagas.objects.get(id=cod)
        vaga.candidato_aceito_id = candidato.id
        vaga.status = 'O'
        vaga.save()
        candidato.save()
        messages.info(request, 'Candidato aceito na vaga')
        return redirect('vagas:login')


class HomeSuper(generic.TemplateView):
    template_name = 'home_super.html'


class SuperUser(CreateView):
    template_name = 'SuperUserPage.html'
    model = Vagas
    fields = ['empresa', 'cargo', 'descricao']
    success_url = reverse_lazy("vagas:homePage")
    # def get(self, request):
    #     render(request, self.template_name)
    #
    #
    # def post(self, request):
    #     form_vagas = VagasForm
    #
    #     form_vagas.is_valid()
