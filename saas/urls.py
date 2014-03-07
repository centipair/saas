from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'saas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'centipair.core.views.home', name='home'),
    url(r'^pricing$', 'centipair.core.views.core_pricing', name='pricing'),
    url(r'^cdn/(?P<source>.+)$', 'centipair.core.views.cdn_redirect',
        name='cdn_redirect'),
    url(r'^core-cdn/(?P<source>.+)$', 'centipair.core.views.core_cdn_redirect',
        name='core_cdn_redirect'),
    url(r'^admin/', include(admin.site.urls)),
)
