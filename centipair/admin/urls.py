from django.conf.urls import patterns, url
from centipair.admin.views import *

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'saas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', AdminHome.as_view(), name='admin-home'),
    url(r'^dashboard$', Dashboard.as_view(), name='dashboard'),
    url(r'^sites$', Sites.as_view(), name='sites'),
    url(r'^site/edit/(?P<site_id>\d+)$', SitePage.as_view(), name='sites'),
)
