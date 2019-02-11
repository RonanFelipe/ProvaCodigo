from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse

from provaDeConceito import settings

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            first_name,
            last_name,
            password=None
    ):
        """
        Cria e salva um usuário com o email, primeiro nome, último nome, data de nascimento e senha.
        """
        if not email:
            raise ValueError("Nome de usuário deve ser um email")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            first_name,
            last_name,
            password
    ):
        """
        Cria e salva superuser, com email, primeiro nome, último nome, data de nascimento e senha.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Endereço de e-mail", max_length=255, unique=True)
    first_name = models.CharField(verbose_name="Primeiro nome", max_length=255)
    last_name = models.CharField(verbose_name="Sobrenome", max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        """Método para tratar se o usuário possui permissões especiais"""
        return True

    def has_module_perms(self, app_label):
        """Método para tratar se o usuário possui permissão para ver a label app"""
        return True

    @property
    def is_staff(self):
        """Se o usuário for um membro do staff?"""
        return self.is_admin


class Empresa(models.Model):
    empresa = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cnpj = models.BigIntegerField(verbose_name="CNPJ da empresa")
    atividade = models.CharField(verbose_name="Atividade principal da empresa", max_length=255)
    nome_empresa = models.CharField(verbose_name="Nome da Empresa", max_length=255)

    def __str__(self):
        return self.nome_empresa


class Candidato(models.Model):
    ESCOLARIDADE = (
        ("1", "Sem escolaridade"),
        ("2", "Primário"),
        ("3", "Ensino Fundamental"),
        ("4", "Ensino Médio"),
        ("5", "Ensino Superior"),
        ("6", "Pos Graduação ou MBA"),
        ("7", "Mestrado"),
        ("8", "Doutorado"),
        ("9", "PHD - Pós Doutorado")
    )
    candidato = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pretensao_salarial = models.FloatField(verbose_name="Pretensão salarial")
    experiencia = models.TextField(verbose_name="Experiência do usuário", max_length=500)
    escolaridade = models.CharField(verbose_name="Nível de escolaridade", max_length=1, choices=ESCOLARIDADE,
                                    blank=True, null=True)


class Vaga(models.Model):
    FAIXA_SALARIAL = (
        ("1", "Até R$ 1000,00"),
        ("2", "De R$ 1000,00 a R$ 2000,00"),
        ("3", "De R$ 2000,00 a R$ 3000,00"),
        ("4", "Acima de R$ 4000,00"),
    )
    ESCOLARIDADE = (
        ("1", "Ensino Fundamental"),
        ("2", "Ensino Médio"),
        ("3", "Tecnológo"),
        ("4", "Ensino Superior"),
        ("5", "Pos Graduação, MBA, Mestrado"),
        ("6", "Doutorado"),
    )
    nome_vaga = models.CharField(verbose_name="Descrição da vaga", max_length=255)
    faixa_salaria = models.CharField(verbose_name="Faixa Salarial", max_length=1, choices=FAIXA_SALARIAL)
    requisitos = models.CharField(verbose_name="Requisitos", max_length=500)
    escolaridade_min = models.CharField(verbose_name="Escolaridade Minima", max_length=1, choices=ESCOLARIDADE)
    empresa_responsavel = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('vaga_details', args=[str(self.id)])

    def __str__(self):
        return self.nome_vaga


class InscricaoVaga(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    mensagem = models.CharField(verbose_name="Mensagem ao recrutador", max_length=255)

    def __str__(self):
        return self.candidato.candidato.name + " - " + self.vaga.nome_vaga
