from django.contrib import admin
from .models import Cep


@admin.register(Cep)
class CepAdmin(admin.ModelAdmin):
    list_display = ('cep', 'logradouro', 'bairro')
    search_fields = ('logradouro', 'bairro')
