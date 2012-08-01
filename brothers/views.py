from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.http import HttpResponseRedirect

from brothers.models import Brother,BrotherEditForm

import sys
import csv

def index(request):
    """Active brother listing."""
    currentPledgeYears = sorted(
        list(
            set(
                [b.pledge_year for b in Brother.objects.filter(active = True)]
                )), reverse = False)

    return render(request, 'brothers/index.html',
                  {'brothers_alist': [(yr, Brother.objects.filter(pledge_year = yr))
                                      for yr in currentPledgeYears]})

def details(request, first_name, last_name):
    return render(request, 'brothers/details.html',
                  {'brother': Brother.objects.get(first_name=first_name, last_name=last_name)})

def register(request):
    if request.method == "POST":
        uform = UserCreationForm(request.POST, instance=User())
        bform = BrotherEditForm(request.POST, request.FILES, instance=Brother())
        if uform.is_valid() and bform.is_valid():
            user         = uform.save()
            brother      = bform.save(commit=False)
            brother.user = user
            brother.save()
            return HttpResponseRedirect('{}_{}'.format(brother.first_name, brother.last_name))
    else:
        uform = UserCreationForm()
        bform = BrotherEditForm()

    return render(request, 'brothers/register.html', {
            'uform': uform,
            'bform': bform,
            })

@login_required
def edit(request):
    brother = request.user.get_profile()
    if request.method == "POST":
        print request.POST
        form = BrotherEditForm(request.POST, request.FILES, instance = brother)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('edit')
    else:
        form = BrotherEditForm(instance = brother)

    return render(request, 'brothers/edit.html', {
            'form': form,
            })

def generate(request):
    dir = sys.path[0]
    reader = csv.reader(open(dir + '/brothers/brothers.csv','rb'))
    for brother in reader:
      dbBrother = Brother()
      email = brother[0] + '@mit.edu'
      user = User.objects.create_user(brother[0],email, brother[1])
      user.save()
      dbBrother.user = user
      name = brother[2]
      dbBrother.first_name = name.split(' ')[0]
      dbBrother.last_name = ' '.join(name.split(' ')[1:])
      dbBrother.email = email
      dbBrother.grad_year = brother[4]
      dbBrother.pledge_year = brother[4]
      dbBrother.active = True
      dbBrother.officer_positions = brother[6]
      dbBrother.majors = brother[5]
      dbBrother.save()
