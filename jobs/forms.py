from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Empresa, Candidato

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class SignUpFormEmpresa(forms.ModelForm):
    class Meta:
        model = Empresa
        exclude = ('empresa',)
