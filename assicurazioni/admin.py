from django.contrib import admin
from assicurazioni.models import *
from django.forms import *

# Register your models here.


class TargaInline(admin.TabularInline):
    model = Targa
    extra = 1


@admin.register(Compagnia)
class CompagniaAdmin(admin.ModelAdmin):
    pass


@admin.register(Polizza)
class PolizzaAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        #print "request DAL : " , aform['dal'].fieldset
        #applicare il filtro 
        if db_field.name == "targa":
            kwargs["queryset"] = Targa.objects.filter(mezzo__modello_id=1)
        return super(PolizzaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_targhe(self, obj):
        return ', '.join(x.numero for x in obj.targa.all())
    get_targhe.short_description = 'Targhe'

    list_display = ('get_targhe', 'compagnia', 'dal', 'al')
    inline = [TargaInline]
    list_filter = ('compagnia',)

