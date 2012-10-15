from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from delta_accounts.views import AccountView, entry_request, entry_approval, assign_fine

urlpatterns = patterns(
    'delta_accounts.views',
    url(r'^$', login_required(AccountView.as_view()), name="delta"),
    url(r'^entry_request/$', entry_request, name="entry_request"),
    url(r'^entry_approval/$', entry_approval, name="entry_approval"),
    url(r'^assign_fine/$', assign_fine, name="assign_fine"),
    url(r'^add_entry/$', 'add_entry', name="add_entry"),
    url(r'^account_index/$', 'account_index', name='account_index'),
    url(r'^account/(?P<pk>[0-9]+)$', 'view_account', name='delta_account'),
    )
