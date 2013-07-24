import re
from django.conf.urls import url, patterns, include
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.template import add_to_builtins

add_to_builtins('avocado.templatetags.avocado_tags')

admin.autodiscover()

urlpatterns = patterns('',
    # Landing Page
    url(r'^$', '{{ project_name }}.views.landing', name='landing'),

    # Cilantro Pages
    url(r'^query/', TemplateView.as_view(template_name='index.html'), name='query'),
    url(r'^results/', TemplateView.as_view(template_name='index.html'), name='results'),

    # Serrano-compatible Endpoint
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
