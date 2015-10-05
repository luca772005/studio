from django.db import models


# Create your models here.


class Tipo(models.Model):
    descrizione = models.CharField(blank=False, null=False, max_length=128)

    def __unicode__(self):
        return "{}".format(self.descrizione)

    class Meta:
        verbose_name_plural = 'Tipi'


class Marca(models.Model):
    descrizione = models.CharField(blank=False, null=False, max_length=128)

    def __unicode__(self):
        return "{}".format(self.descrizione)

    class Meta:
        verbose_name_plural = 'Marche'


class Modello(models.Model):
    descrizione = models.CharField(blank=False, null=False, max_length=128)
    marca = models.ForeignKey(Marca, null=False, blank=False)
    tipo = models.ForeignKey(Tipo, null=False, blank=False)

    def __unicode__(self):
        return "{}".format(self.descrizione)

    class Meta:
        verbose_name_plural = 'Modelli'


class Alimentazione(models.Model):
    descrizione = models.CharField(blank=False, null=False, max_length=128)

    def __unicode__(self):
        return "{}".format(self.descrizione)

    class Meta:
        verbose_name_plural = 'Alimentazioni'


class Mezzo(models.Model):
    telaio = models.CharField(blank=False, null=False, max_length=128)
    colore = models.CharField(blank=False, null=False, max_length=128)
    alimentazione = models.ForeignKey(Alimentazione, null=False, blank=False)
    modello = models.ForeignKey(Modello, null=False, blank=False)

    def __unicode__(self):
        return "{} {}".format(self.telaio, self.modello)

    class Meta:
        verbose_name_plural = 'Mezzi'


class Targa(models.Model):
    numero = models.CharField(null=False, blank=False, max_length=16)
    dal = models.DateField()
    al = models.DateField()
    mezzo = models.ForeignKey(Mezzo, null=False, blank=False)

    def __unicode__(self):
        return "{}".format(self.numero)

    class Meta:
        verbose_name_plural = 'Targhe'
