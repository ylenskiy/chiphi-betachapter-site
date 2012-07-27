from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'brothers.views',
    url(r'^$', 'index', name="brothers"),
    url(r'^(?P<first_name>.+)_(?P<last_name>.+)$', 'details'),
    url(r'^register', 'register'),
    url(r'^edit', 'edit', name='edit_profile'),
    )

urlpatterns += patterns(
    '',
    url(r'^login', 'django.contrib.auth.views.login',
        {'template_name': 'brothers/login.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', 
        {'template_name': 'brothers/logout.html'}, name='logout'),
    )