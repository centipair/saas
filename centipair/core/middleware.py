#from django.http import HttpResponse
from centipair.core.models import Site, SiteUser
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import ugettext as _


class SiteUserMirror(object):
    def __init__(self, request, site, *args, **kwargs):
        site_user = self.get_site_user(request, site)
        if site_user:
            self.username = site_user.username
            self.role = site_user.role
            self.exists = True
        else:
            self.exists = False

    def get_site_user(self, request, site):
        #TODO: implement cache layer
        site_user = None
        if request.user.is_authenticated():
            try:
                site_user = SiteUser.objects.get(user=request.user,
                                                 site=site)
            except SiteUser.DoesNotExist:
                site_user = None

        return site_user


class SiteMirror(object):
    """
    Class for site object used in request
    Instance contains site and Site User details
    """
    def __init__(self, request, *args, **kwargs):
        self.exists = False
        site = self.get_site(request)
        if not site:
            return
        self.id = site.id
        self.exists = True
        self.name = site.name
        self.domain_name = site.domain_name
        self.service_domain_name = site.service_domain_name
        self.store_domain_name = site.store_domain_name
        self.blog_domain_name = site.blog_domain_name
        self.support_domain_name = site.support_domain_name
        self.template_dir = site.template_dir
        self.is_core = site.is_core
        self.site_user = SiteUserMirror(request, site)

    def get_site(self, request):
    #TODO: Implement cache layer.
        try:
            domain_name = request.META["HTTP_HOST"].split(":")[0]
            site_obj = Site.objects.get(
                Q(domain_name=domain_name) |
                Q(service_domain_name=domain_name) |
                Q(store_domain_name=domain_name) |
                Q(blog_domain_name=domain_name) |
                Q(support_domain_name=domain_name))
            return site_obj
        except Site.DoesNotExist:
            return None

    def not_found(self):
        return HttpResponse(_('Not found'), status=404)


class SiteMiddleware:
    """Inject the site object to request based on domain name"""
    def process_request(self, request):
        site = SiteMirror(request)
        if not site.exists:
            return site.not_found()
        else:
            request.site = site


class ApiMiddleware:
    def process_request(self, request):
        return
