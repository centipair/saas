#from django.http import HttpResponse
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.conf import settings
from centipair.core.cache import get_app_cache, get_site_cache,\
    get_site_apps_cache


class AppMirror(object):
    def __init__(self, request, app_dict, *args, **kwargs):
        self.template_name = app_dict["template_name"]
        self.template_dir = app_dict["template_dir"]
        self.app = app_dict["app"]
        self.domain_name = app_dict["domain_name"]
        self.site_id = app_dict["site_id"]


class SiteMirror(object):
    """
    Class for site object used in request
    Instance contains site and Site User details
    """
    def __init__(self, request, *args, **kwargs):
        domain_name = request.META["HTTP_HOST"].split(":")[0]
        if 'www.' in domain_name:
            domain_name = domain_name.replace('www.', '')
        self.exists = False
        app = get_app_cache(domain_name)
        if not app:
            return None
        self.exists = True
        self.requested_app = AppMirror(app)
        site = get_site_cache(app["site_id"])
        self.id = site["id"]
        self.name = site["name"]
        self.template_dir = site["template_dir"]
        self.apps = get_site_apps_cache()

    def not_found(self):
        return HttpResponse(_('Not found'), status=404)


class SiteMiddleware:
    """Inject the site object to request based on domain name"""
    def process_request(self, request):
        site = SiteMirror(request)
        if site.exists:
            request.site = site
        else:
            return site.not_found()
