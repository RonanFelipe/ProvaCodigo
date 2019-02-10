from django.urls import path
from . import views as jobs_views


urlpatterns = [
    path('', jobs_views.index, name='index'),
    path('createEmpresa/', jobs_views.signup_empresa, name='empresa_signup'),
    path('createCandidato/', jobs_views.signup_candidato, name='candidato_signup'),
    path('home/', jobs_views.home, name='home'),
]
