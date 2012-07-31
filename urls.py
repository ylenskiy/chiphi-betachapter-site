from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static  import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

# Root-level urls
urlpatterns = patterns(
    'views',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name="contact"),
    url(r'^house/$', TemplateView.as_view(template_name='house.html'), name="house"),
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

# When debugging, serve media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
