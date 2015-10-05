from django.db import models
from aziende.models import *

# Create your models here.


class Anagrafica(models.Model):
    nome = models.CharField(null=False, max_length=128)
    cognome = models.CharField(null=False, max_length=128)
    codice_fiscale = models.CharField(null=False, max_length=16)
    azienda = models.ManyToManyField(Azienda, through='AnagraficaAzienda')

    def __unicode__(self):
        return "{} {}".format(self.cognome, self.nome)

    class Meta:
        verbose_name_plural = 'Anagrafica'


class AnagraficaAzienda(models.Model):
    anagrafica = models.ForeignKey(Anagrafica)
    azienda = models.ForeignKey(Azienda)
    dal = models.DateField()
    al = models.DateField()
    orario = models.CharField(null=False, max_length=128)

    class Meta:
        verbose_name_plural = 'Rapporti di lavoro'