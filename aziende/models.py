from django.db import models

# Create your models here.


class Azienda(models.Model):
    nome = models.CharField(null=False, max_length=128)

    def __unicode__(self):
        return "{}".format(self.nome)

    class Meta:
        verbose_name_plural = 'Aziende'
