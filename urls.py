from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static  import static
from django.views.generic import TemplateView,DetailView
from site_content.models import StaticContent

from django.contrib import admin
admin.autodiscover()

# Root-level urls
urlpatterns = patterns(
    'views',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^rush/$', TemplateView.as_view(template_name='rush.html'), name="rush"),
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

# Static menu urls
urlpatterns += patterns(
    '',
    url(r'^rush/(?P<slug>[-_\w]+)',
        DetailView.as_view(model = StaticContent, template_name = "rush.html"), name = "rush"),
    url(r'^involvement/(?P<slug>[-_\w]+)',
        DetailView.as_view(model = StaticContent, template_name = "involvement.html"), name = "involvement"),
    url(r'^about/(?P<slug>[-_\w]+)',
        DetailView.as_view(model = StaticContent, template_name = "about.html"), name = "about"),
    url(r'^history/(?P<slug>[-_\w]+)',
        DetailView.as_view(model = StaticContent, template_name = "history.html"), name = "history"),
    url(r'^contact$',
        DetailView.as_view(model = StaticContent, template_name = "contact.html"), {'slug':'Contact'}, name = "contact"),

)

# When debugging, serve media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
