from delta_accounts.models import DeltaEntry, EntryRequestForm, FineForm
from brothers.models import Brother
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
        form = EntryRequestForm(request.POST)
        if form.is_valid():
            form.clean()
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
            form.clean()
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
