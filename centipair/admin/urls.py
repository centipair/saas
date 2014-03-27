from django.conf.urls import patterns, url
from centipair.admin.views import Dashboard

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'saas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', Dashboard.as_view(), name='dashboard'),
)
