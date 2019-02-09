from django.urls import path
from . import views as jobs_views


urlpatterns = [
    path('', jobs_views.index, name='home'),
]
