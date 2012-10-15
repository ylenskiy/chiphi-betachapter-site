from brothers.models import Brother
from delta_accounts.models import DeltaEntry, EntryRequestForm, FineForm, EntryForm

from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory

class AccountView(ListView):
    template_name = "delta/account.html"
    context_object_name = "account"

    def get_queryset(self):
        return DeltaEntry.objects.filter(user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context['balance'] = sum([entry.amount for entry in context['account'] if entry.approved])
        if context['balance'] < 0:
            context['balance_string'] = "-${}".format(abs(context['balance']))
        else:
            context['balance_string'] = "${}".format(context['balance'])
        return context

@login_required
def entry_request(request):
    if request.method == "POST":
        form = EntryRequestForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.approved = None
            entry.save()
            return HttpResponseRedirect('/delta/')
    else:
        form = EntryRequestForm()
    return render(request, 'delta/entry_request.html', {
            'form': form,
            })

@permission_required('delta_accounts.can_approve_entries')
def entry_approval(request):
    if request.method == "POST":
        for (k,v) in request.POST.items():
            if k.isdigit():
                entry = DeltaEntry.objects.get(pk=k)
                if v == 'approve':
                    entry.approved = True
                elif v == 'deny':
                    entry.approved = False
                entry.save()
    requests = DeltaEntry.objects.filter(approved = None)
    if not(request.user.has_perm('delta_accounts.can_add_entries')):
        requests = requests.exclude(user = request.user)
    return render(request, 'delta/entry_approval.html', {
            'requests': requests
            })

@permission_required('delta_accounts.can_assign_fines')
def assign_fine(request):
    if request.method == "POST":
        form = FineForm(request.POST)
        if form.is_valid():
            fine = form.save(commit = False)
            fine.approved = True
            fine.user = Brother.objects.get(pk = request.POST.get('brother')).user
            fine.amount = -1 * abs(fine.amount)
            fine.save()
            return HttpResponseRedirect('/delta/assign_fine')
    else:
        form = FineForm()
    return render(request, 'delta/assign_fine.html', {
            'actives': Brother.objects.filter(active = True),
            'form': form,
            })

@permission_required('delta_accounts.can_add_entries')
def add_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit = False)
            entry.approved = True
            entry.user = Brother.objects.get(pk = request.POST.get('brother')).user
            entry.save()
            return HttpResponseRedirect('/delta/add_entry/')
    else:
        form = EntryForm()
    return render(request, 'delta/add_entry.html', {
            'actives': Brother.objects.filter(active = True),
            'form': form,
            })

@permission_required('delta_accounts.can_add_entries')
def account_index(request):
    currentPledgeYears = sorted(
        list(
            set(
                [b.pledge_year for b in Brother.objects.filter(active = True)]
                )), reverse = False)
    return render(request, 'delta/account_index.html', {
            'year_brothers': [(yr, Brother.objects.filter(pledge_year = yr, active = True))
                              for yr in currentPledgeYears],
            })

@permission_required('delta_accounts.can_add_entries')
def view_account(request, pk):
    brother = Brother.objects.get(pk = pk)
    queryset = DeltaEntry.objects.filter(user=brother.user)
    EntryFormSet = modelformset_factory(DeltaEntry, exclude=('user'), can_delete=True)
    if request.method == "POST":
        formset = EntryFormSet(request.POST, request.FILES, queryset = queryset)
        if formset.is_valid():
            entries = formset.save(commit=False)
            for entry in entries:
                entry.user = brother.user
                entry.save()
            return HttpResponseRedirect('/delta/account/{}'.format(pk))
    else:
        formset = EntryFormSet(queryset = queryset,
                               initial = [{
                    'approved': True
                    }])
    return render(request, 'delta/view_account.html', {
            'brother': brother,
            'formset': formset,
            'balance': brother.getBalance(),
            })
