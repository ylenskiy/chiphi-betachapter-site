from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# Root-level urls
urlpatterns = patterns(
    'chiphi_betachapter.views',
    url(r'^$', 'home', name="home"),
    url(r'^contact/$', 'contact', name="contact"),
    url(r'^house/$', 'house', name="house"),
)

# Admin-related urls
urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    )

# App-related urls
urlpatterns += patterns(
    '',
    url(r'^brothers/', include('brothers.urls')),
)
