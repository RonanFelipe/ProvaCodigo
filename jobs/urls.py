from django.urls import path
from . import views as jobs_views


urlpatterns = [
    path('', jobs_views.index, name='index'),
    path('createEmpresa/', jobs_views.signup_empresa, name='empresa_signup'),
    path('createCandidato/', jobs_views.signup_candidato, name='candidato_signup'),
    path('home/', jobs_views.home, name='home'),
    path('homeEmpresa/', jobs_views.home_empresa, name='home_to_empresa'),
    path('homeCandidato/', jobs_views.home_candidato, name='home_to_candidato'),
    path('<int:pk>/inscrever', jobs_views.inscrever_vaga, name='inscrever_vaga'),
    path('vaga/', jobs_views.VagaListView.as_view(), name='vagas'),
    path('vaga/<int:pk>', jobs_views.VagaDetail.as_view(), name='vaga_details'),
    path('vaga/create/', jobs_views.CreateVaga.as_view(), name='create_vaga'),
    path('vaga/<int:pk>/update/', jobs_views.UpdateVaga.as_view(), name='update_vaga'),
    path('vaga/<int:pk>/delete/', jobs_views.DeleteVaga.as_view(), name='delete_vaga'),
    path('errorDuplicate/', jobs_views.error_duplicate, name='duplicate'),
    path('inscricoesFeitas/', jobs_views.InscricoesVagasListView.as_view(), name='inscricoes_feitas'),
    path('vagaDetail/<int:pk>', jobs_views.VagaDetailEmpresa.as_view(), name='vaga_empresa_details'),

]
