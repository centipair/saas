from django.conf.urls import patterns, url
from centipair.admin.views import AdminHome, Dashboard

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'saas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', AdminHome.as_view(), name='admin-home'),
    url(r'^dashboard$', Dashboard.as_view(), name='dashboard'),
)
