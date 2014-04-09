from django.conf.urls import patterns, include, url
from centipair.core.views import RegistrationView, LoginView
from rest_framework import routers
from centipair.core import api_views


router = routers.DefaultRouter()
router.register(r'users-urls', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)


#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'saas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'centipair.core.views.home', name='home'),
    url(r'^register$', RegistrationView.as_view(), name='registration'),
    url(r'^login/?$', LoginView.as_view(), name='login'),
    url(r'^logout/?$', 'centipair.core.views.logout_view', name='logout'),
    url(r'^pricing$', 'centipair.core.views.core_pricing', name='pricing'),
    url(r'^cdn/(?P<source>.+)$', 'centipair.core.views.cdn_redirect',
        name='cdn_redirect'),
    url(r'^core-cdn/(?P<source>.+)$', 'centipair.core.views.core_cdn_redirect',
        name='core_cdn_redirect'),
    url(r'^admin/', include('centipair.admin.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^(?P<url>.+)$', 'centipair.cms.views.page', name='page'),
)
