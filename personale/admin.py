from django.contrib import admin
from personale.models import Anagrafica, AnagraficaAzienda
from aziende.models import Azienda

# Register your models here.


class AnagraficaAziendaInline(admin.TabularInline):
    model = AnagraficaAzienda
    extra = 1


@admin.register(Anagrafica)
class AnagraficaAdmin(admin.ModelAdmin):
    def lista_aziende(self, obj):
        return ', '.join(x.azienda.nome for x in obj.anagraficaazienda_set.all())

    list_display = ('codice_fiscale', 'cognome', 'nome', 'lista_aziende')
    
    inlines = [AnagraficaAziendaInline]


