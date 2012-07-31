from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver

from django.forms import ModelForm

def getImageFileName(instance, filename):
    from os.path import splitext,join
    ext = splitext(filename)[-1]
    return join('portraits', str(instance.pledge_year), instance.first_name + '_' + instance.last_name + ext)

class Brother(models.Model):
    user        = models.OneToOneField(User, primary_key = True, editable = False)

    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    email       = models.EmailField()
    grad_year   = models.SmallIntegerField(verbose_name = 'Graduation year')
    pledge_year = models.SmallIntegerField(verbose_name = 'Pledge class year')
    active      = models.BooleanField(verbose_name = 'Active status', default = True)

    portrait    = models.FileField(upload_to=getImageFileName, blank=True)
    hometown    = models.CharField(max_length=200, blank=True)
    majors      = models.CharField(max_length=300, verbose_name = 'Major(s)', blank=True)
    profile     = models.TextField(verbose_name = 'Optional bio/interests description', blank=True)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class BrotherEditForm(ModelForm):
    class Meta:
        model = Brother
