#from django.http import HttpResponse
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.conf import settings
from centipair.core.cache import AppMirror, get_app_cache, get_site_cache,\
    get_site_apps_cache, get_site_app_cache, get_site_user_cache


class SiteMirror(object):
    """
    Class for site object used in request
    Instance contains site and Site User details
    """
    def __init__(self, request, *args, **kwargs):
        self.exists = False
        domain_name = request.META["HTTP_HOST"].split(":")[0]
        if 'www.' in domain_name:
            domain_name = domain_name.replace('www.', '')
        app = get_app_cache(domain_name)
        if not app:
            return None
        self.exists = True
        self.requested_domain_name = domain_name
        site = get_site_cache(app["site_id"])
        if site["domain_name"] == app["domain_name"]:
            # default app
            app = get_site_app_cache(site["id"], site["default_app"])

        self.requested_app = AppMirror(app)
        self.id = site["id"]
        self.name = site["name"]
        self.template_dir = site["template_dir"]
        self.domain_name = site["domain_name"]
        self.apps = get_site_apps_cache(self.id)

    def not_found(self):
        return HttpResponse(_('Not found'), status=404)


class SiteMiddleware:
    """Inject the site object to request based on domain name"""
    def process_request(self, request):
        site = SiteMirror(request)
        if site.exists:
            request.site = site
            request.site_user = get_site_user_cache(request)
        else:
            return site.not_found()
