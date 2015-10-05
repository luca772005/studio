from django.contrib import admin
from aziende.models import Azienda

# Register your models here.

@admin.register(Azienda)
class AziendaAdmin(admin.ModelAdmin):
    pass