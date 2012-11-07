import re
from django.conf.urls import url, patterns, include
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.template import add_to_builtins

add_to_builtins('avocado.templatetags.avocado_tags')

admin.autodiscover()

urlpatterns = patterns('',
    # Home/Splash/Index page
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    # Mount point for the Cilantro app. Since this is a single-page web app
    # all URLs will be routed relative to this endpoint.
    url(r'^workspace/', 'cilantro.views.app', name='cilantro'),

    # Other Cilantro endpoints such as the preferences/session API
    url(r'^', include('cilantro.urls')),

    # Serrano API endpoints
    url(r'^api/', include('serrano.urls')),

    # Administrative components
    url(r'^admin/', include(admin.site.urls)),
)

# In production, these two locations must be served up statically
urlpatterns += patterns('django.views.static',
    url(r'^{0}(?P<path>.*)$'.format(re.escape(settings.MEDIA_URL.lstrip('/'))), 'serve', {
        'document_root': settings.MEDIA_ROOT
    }),
    url(r'^{0}(?P<path>.*)$'.format(re.escape(settings.STATIC_URL.lstrip('/'))), 'serve', {
        'document_root': settings.STATIC_ROOT
    }),
)
