from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import SignUpForm, SignUpFormEmpresa, SignUpFormCandidato, IncreverVagaForm
from .models import Vaga, InscricaoVaga, Candidato, Empresa


# Create your views here.
def index(request):
    return render(request, 'base.html')


def success(request):
    return render(request, 'success.html')


def home_candidato(request):
    return render(request, 'homeCandidato.html')


def home_empresa(request):
    return render(request, 'homeEmpresa.html')


@login_required(login_url='/accounts/login')
def home(request):
    try:
        if Candidato.objects.get(candidato=request.user):
            return redirect('home_to_candidato')
    except Candidato.DoesNotExist:
        pass
    try:
        if Empresa.objects.get(empresa=request.user):
            return redirect('home_to_empresa')
    except Empresa.DoesNotExist:
        return redirect('login')


def signup_empresa(request):
    if request.method == 'POST':
        form1 = SignUpForm(request.POST)
        form2 = SignUpFormEmpresa(request.POST)
        if all([form1.is_valid(), form2.is_valid()]):
            model1 = form1.save()
            model2 = form2.save(commit=False)
            model2.empresa = model1
            model2.save()
            return redirect('home')
    else:
        form1 = SignUpForm()
        form2 = SignUpFormEmpresa()
    return render(request, 'createEmpresa.html', {'form1': form1, 'form2': form2})


def signup_candidato(request):
    if request.method == 'POST':
        form1 = SignUpForm(request.POST)
        form2 = SignUpFormCandidato(request.POST)
        if all([form1.is_valid(), form2.is_valid()]):
            model1 = form1.save()
            model2 = form2.save(commit=False)
            model2.candidato = model1
            model2.save()
            return redirect('home')
    else:
        form1 = SignUpForm()
        form2 = SignUpFormCandidato()
    return render(request, 'createCandidato.html', {'form1': form1, 'form2': form2})


class VagaListView(generic.ListView):
    model = Vaga


class VagaDetail(generic.DetailView):
    model = Vaga


class CreateVaga(CreateView):
    model = Vaga
    fields = '__all__'
    success_url = reverse_lazy('vagas')


class UpdateVaga(UpdateView):
    model = Vaga
    fields = ['nome_vaga', 'faixa_salaria', 'requisitos', 'escolaridade_min']


class DeleteVaga(DeleteView):
    model = Vaga
    success_url = reverse_lazy('vagas')


def inscrever_vaga(request, pk):
    if request.method == 'POST':
        try:
            inscricao = InscricaoVaga()
            inscricao.vaga = Vaga.objects.get(id=pk)
            inscricao.candidato = Candidato.objects.get(candidato=request.user)
            inscricao.save()
        except IntegrityError as e:
            return redirect("duplicate")
    return redirect('vagas')


def error_duplicate(request):
    return render(request, 'duplicate_error.html')


class InscricoesVagasListView(generic.ListView):
    model = InscricaoVaga
    template_name = 'jobs/vagas_com_inscricoes.html'

    def get_queryset(self):
        return InscricaoVaga.objects.all()
