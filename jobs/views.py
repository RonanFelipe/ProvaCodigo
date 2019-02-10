from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import SignUpForm, SignUpFormEmpresa, SignUpFormCandidato
from .models import Vaga


# Create your views here.
def index(request):
    return render(request, 'base.html')


def success(request):
    return render(request, 'success.html')


@login_required(login_url='/accounts/login')
def home(request):
    return render(request, 'success.html')


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
    paginate_by = 10


class VagaDetail(generic.DetailView):
    model = Vaga


class CreateVaga(CreateView):
    model = Vaga
    fields = '__all__'


class UpdateVaga(UpdateView):
    model = Vaga
    fields = ['nome_vaga', 'faixa_salaria', 'requisitos', 'escolaridade_min']


class DeleteVaga(DeleteView):
    model = Vaga
    success_url = reverse_lazy('vagas')
