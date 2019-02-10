from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import SignUpForm, SignUpFormEmpresa, SignUpFormCandidato


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
