from django.urls import path, include
from vagasApp import views
from .api import urls

app_name = 'vagas'
urlpatterns = [
    path('', views.TemplateHome.as_view(), name='home'),
    path('register/', views.CandidatoViewRegister.as_view(), name='register'),
    path('login/', views.CandidatoViewLogin.as_view(), name='login'),
    path('homepage/', views.HomePageCandidato.as_view(), name='homePage'),
    path('homesuper/', views.HomeSuper.as_view(), name='home_super'),
    path('acept/', views.AceitarCandidato.as_view(), name='acept'),
    path('super/', views.SuperUser.as_view(), name='super'),
    path('curriculum/', views.CurriculumView.as_view(), name='curriculum'),
    path('api/', include(urls))
]
