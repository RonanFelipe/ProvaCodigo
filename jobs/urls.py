from django.urls import path
from . import views as jobs_views


urlpatterns = [
    path('', jobs_views.index, name='index'),
    path('createEmpresa/', jobs_views.signup_empresa, name='empresa_signup'),
]
