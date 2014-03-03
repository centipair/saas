#from django.http import HttpResponse
from core.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404


class SiteMiddleware:
    def process_request(self, request):
        domain_name = request.META["HTTP_HOST"].split(":")[0]

        try:
            site_obj = Site.objects.get(Q(domain_name=domain_name) |
                                        Q(service_domain_name=domain_name))
            request.site = site_obj
        except ObjectDoesNotExist:
            return Http404


class ApiMiddleware:
    def process_request(self, request):
        return
