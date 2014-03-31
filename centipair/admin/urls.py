from django.conf.urls import patterns, url
from centipair.admin.views import *

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'saas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', AdminHome.as_view(), name='admin-home'),
    url(r'^404$', Admin404.as_view(), name='admin-404'),
    url(r'^dashboard$', Dashboard.as_view(), name='dashboard'),
    url(r'^sites$', SitesPage.as_view(), name='sites'),
    url(r'^sites/mine$', SitesMineData.as_view(), name='sites-mine'),
    url(r'^sites/edit/(?P<id>\d+)?$', SitesEdit.as_view(), name='site-edit'),
    url(r'^sites/app/edit/(?P<id>\d+)?$', AppEdit.as_view(), name='app-edit'),
)
