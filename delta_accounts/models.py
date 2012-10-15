from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class DeltaEntry(models.Model):
    user        = models.ForeignKey(User)
    
    amount      = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=1000)
    evidence    = models.FileField(upload_to='reciepts', blank=True)
    
    approved    = models.NullBooleanField(default = None)

    created     = models.DateTimeField(auto_now_add=True)

    def is_debt(self):
        return (self.amount < 0)
    def is_credit(self):
        return (self.amount > 0)

    def amount_string(self):
        s = "${}".format(abs(self.amount))
        if self.is_debt():
            return "-{}".format(s)
        else:
            return s

    class Meta:
        permissions = (
            ('can_approve_entries', 'Can approve delta entries.'),
            ('can_assign_fines', 'Can assign delta fines.'),
            )

class EntryRequestForm(ModelForm):
    class Meta:
        model = DeltaEntry
        exclude = ('user', 'approved', 'created')

class FineForm(ModelForm):
    class Meta:
        model = DeltaEntry
        exclude = ('user', 'approved', 'created')
