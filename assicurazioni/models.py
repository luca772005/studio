from django.db import models
from targhe.models import *

# Create your models here.


class Compagnia(models.Model):
    descrizione = models.CharField(null=False, blank=False, max_length=128)

    def __unicode__(self):
        return "{}".format(self.descrizione)

    class Meta:
        verbose_name_plural = 'Compagnie'

class Polizza(models.Model):
    protocollo = models.CharField(null=True, blank=True, max_length=128)
    compagnia = models.ForeignKey(Compagnia, null=False, blank=False)
    broker = models.CharField(null=True, max_length=128)
    premio = models.DecimalField(max_digits=12, decimal_places=2)
    dal = models.DateField()
    al = models.DateField()
    targa = models.ManyToManyField(Targa)

    def __unicode__(self):
        return "{} : dal {} al {}".format(self.compagnia, self.dal, self.al)

    class Meta:
        verbose_name_plural = 'Polizze'