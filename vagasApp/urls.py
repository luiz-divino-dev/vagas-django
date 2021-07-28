from django.urls import path
from vagasApp import views

app_name ='vagas'
urlpatterns = [
    path('', views.TemplateHome.as_view(), name='home'),
    path('register/', views.CandidatoViewRegister.as_view(), name='register'),
    path('login/', views.CandidatoViewLogin.as_view(), name='login'),
    path('homepage/', views.HomePageCandidato.as_view(), name='homePage'),
    #path('apply/', views.Apply.as_view(), name='apply'),
    path('super/', views.SuperUser.as_view(), name='super'),
    path('curriculum/', views.CurriculumView.as_view(), name='curriculum'),
]
