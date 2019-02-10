from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect
from .forms import SignUpForm, SignUpFormEmpresa


# Create your views here.
def index(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


def signup_empresa(request):
    if request.method == 'POST':
        form1 = SignUpForm(request.POST)
        form2 = SignUpFormEmpresa(request.POST)
        if all([form1.is_valid(), form2.is_valid()]):
            model1 = form1.save()
            model2 = form2.save(commit=False)
            model2.empresa = model1
            model2.save()
            return redirect('index')
    else:
        form1 = SignUpForm()
        form2 = SignUpFormEmpresa()
    return render(request, 'createEmpresa.html', {'form1': form1, 'form2': form2})
