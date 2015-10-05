from django.contrib import admin
from targhe.models import *
from assicurazioni.models import *
from django.contrib.admin import SimpleListFilter
from django.contrib.admin import ModelAdmin
import datetime


# Register your models here.


class TargaInline(admin.TabularInline):
    model = Targa
    extra = 1



@admin.register(Modello)
class ModelloAdmin(admin.ModelAdmin):
    list_display = ('descrizione', 'marca', 'tipo')
    list_filter = ('marca', 'tipo',)

@admin.register(Alimentazione)
class AlimentazioneAdmin(admin.ModelAdmin):
    pass


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    pass

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    pass


class MarcaFilter(SimpleListFilter):
    title = 'marca' # or use _('country') for translated title
    parameter_name = 'marca'

    def lookups(self, request, model_admin):
        #modelli = set([c for c in Modello.objects.all()])
        modelli = set([c.marca for c in Modello.objects.select_related('marca')])
        return [(c.id, c.descrizione) for c in modelli]
        # You can also use hardcoded model name like "Country" instead of 
        # "model_admin.model" if this is not direct foreign key filter

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(modello__marca_id__exact=self.value())
        else:
            return queryset


class TipoFilter(SimpleListFilter):
    title = 'tipo' # or use _('country') for translated title
    parameter_name = 'tipo'

    def lookups(self, request, model_admin):
        #modelli = set([c for c in Modello.objects.all()])
        tipi = set([c.tipo for c in Modello.objects.select_related('tipo')])
        return [(c.id, c.descrizione) for c in tipi]
        # You can also use hardcoded model name like "Country" instead of 
        # "model_admin.model" if this is not direct foreign key filter

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(modello__tipo_id__exact=self.value())
        else:
            return queryset

@admin.register(Mezzo)
#class MezzoAdmin(admin.ModelAdmin):
class MezzoAdmin(ModelAdmin):
    def get_marca(self, obj):
        return obj.modello.marca.descrizione
    get_marca.short_description = 'Marca'

    def get_targa(self, obj):
        return ', '.join(x.numero+'('+str(x.dal)+'/'+str(x.al)+')' for x in obj.targa_set.all())
    get_targa.short_description = 'Targa'

    def get_tipo(self, obj):
           return obj.modello.tipo.descrizione
    get_tipo.short_description = 'Tipo'

    def get_compagnia(self, obj):
        return Polizza.objects.filter(targa__mezzo=obj,
                                      dal__lte=datetime.datetime.now(),
                                      al__gte=datetime.datetime.now())

    list_display = ('telaio', 'get_targa', 'alimentazione',
                    'get_tipo', 'get_marca', 'modello', 'get_compagnia',)
    search_fields = ('telaio', 'modello__descrizione', 'targa__numero',
                     'alimentazione__descrizione')
    inlines = [TargaInline]
    list_filter = (MarcaFilter, TipoFilter,)

