#from django.http import HttpResponse
from centipair.core.models import Site
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import ugettext as _


class SiteMiddleware:
    """Inject the site object to request based on domain name"""
    def process_request(self, request):
        domain_name = request.META["HTTP_HOST"].split(":")[0]

        try:
            site_obj = Site.objects.get(
                Q(domain_name=domain_name) |
                Q(service_domain_name=domain_name) |
                Q(store_domain_name=domain_name) |
                Q(blog_domain_name=domain_name) |
                Q(support_domain_name=domain_name))

            request.site = site_obj
        except Site.DoesNotExist:
            return HttpResponse(_('Not found'), status=404)


class ApiMiddleware:
    def process_request(self, request):
        return
