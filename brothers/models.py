from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from django.forms import ModelForm

from delta_accounts.models import DeltaEntry

class Officer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name = "Officer position description and responsibilities")

    def __unicode__(self): return self.name

def getImageFileName(instance, filename):
    from os.path import splitext,join
    ext = splitext(filename)[-1]
    return join('portraits', str(instance.pledge_year), instance.fullName() + ext)

class Brother(models.Model):
    user        = models.OneToOneField(User, primary_key = True, editable = False)

    name        = models.CharField(max_length=300)
    email       = models.EmailField()
    grad_year   = models.SmallIntegerField(verbose_name = 'Graduation year')
    pledge_year = models.SmallIntegerField(verbose_name = 'Pledge class year')
    active      = models.BooleanField(verbose_name = 'Active status', default = True)

    # Optional fields
    officer_positions = models.ManyToManyField(Officer, blank=True)

    portrait          = models.FileField(upload_to=getImageFileName,                blank=True)
    hometown          = models.CharField(max_length=200,                            blank=True)
    majors            = models.CharField(max_length=300, verbose_name = 'Major(s)', blank=True)
    profile           = models.TextField(verbose_name = 'Bio and interests',        blank=True)

    def getPortraitUrl(self):
        from os.path import join
        if self.portrait.name:
            return self.portrait.url
        else:
            return join(settings.STATIC_URL, "images/default.jpg")

    def isOfficer(self): return self.officer_positions.count() > 0

    def getBalance(self):
        return sum([entry.amount for entry in DeltaEntry.objects.filter(user = self.user, approved = True)])

    def fullName(self):
        return self.name

    def __unicode__(self):
        return self.fullName()

class BrotherEditForm(ModelForm):
    class Meta:
        model = Brother
