from django import views
from django.db import transaction
from django.shortcuts import render, redirect
from vagasApp.forms import CandidatoFormRegister, UserForm, CurriculumForm
from vagasApp.forms.candidato import CurriculumRegisterForm
from vagasApp.models import Curriculum, Candidato
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
    template_name = 'CandidatoLoginTemplate.html'

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
                return redirect('vagas:SuperUserPage')

        else:
            messages.error(request, "Invalid username or password.")

        return render(request, self.template_name)


class TemplateHome(generic.TemplateView):
    template_name = 'Home.html'


class HomePageCandidato(views.View):
    template_name = 'HomePage.html'

    def get(self, request):
        return render(request, self.template_name)

    # def post(self, request):
    #    pass


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


class SuperUser(views.View):
    pass
