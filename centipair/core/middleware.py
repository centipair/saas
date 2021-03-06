#from django.http import HttpResponse
from centipair.core.models import Site, SiteUser, App
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.conf import settings


def select_domain(request):
    return


def user_site_home(request):
    if request.site.requested_app == settings.APPS['CMS']:
        return cms_home(request)
    elif request.site.requested_app == settings.APPS['STORE']:
        return store_home(request)
    else:
        #TODO: render a nice template
        return HttpResponse('App not found', status=404)


def site_home(request):
    if request.site.requested_app == settings.APPS['CORE']:
        return core_home(request)
    else:
        return user_site_home(request)
    return HttpResponse(_('Hello world'))


def cdn_file(request, source):
    site = request.site
    template_path = site.template_dir + "/cdn/" + source
    source_file_url = settings.TEMPLATE_STATIC_URL + "/" + template_path
    return source_file_url


def get_base_path(request, base_file):
    site = request.site
    if site.is_core:
        base_path = settings.CORE_TEMPLATE_PATH + "/" +\
            site.template_dir + "/" + base_file
    else:
        base_path = site.template_dir + "/" + site.template_name + "/" +\
            base_file
    return base_path


def render_core_template(request, template_file, context):
    """Renders core templates """
    template_location = settings.CORE_TEMPLATE_PATH + "/" + template_file
    return render(request, template_location, context)


def render_cms_template(request, template_file, context):
    """Renders core templates """
    site = request.site
    template_dir = settings.CMS_TEMPLATE_PATH + "/" + site.template_name + "/"
    template_location = template_dir + template_file

    return render(request, template_location, context)


def render_template(request, template_file, context={}, app=None, base=None):
    """Renders template based on the site"""

    if app:
        if app == settings.APPS['CORE']:
            return render_core_template(request, template_file, context)
        else:
            return render_app_template(request, template_file, context,
                                       app, base)
    else:
        return render_core_template(request, "app_error.html", context)


def render_template_new(request, template_file, context={}, base=None):
    site = request.site
    #template_location =


def render_app_template(request, template_file, context, app, base):
    site = request.site
    app = App.objects.get(site_id=request.site.id, app=app)
    template_location = site.template_dir + "/" + app.template_dir +\
        "/" + app.template_name + "/" + template_file
    if context:
        context["centipair_base_template"] = base
    else:
        context = {}
        context["centipair_base_template"] = base

    return render(request, template_location, context)


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


class AppMirror(object):
    def __init__(self, app_model, *args, **kwargs):
        self.template_name = app_model.template_name
        self.template_dir = app_model.template_dir
        self.app = app_model.app
        self.domain_name = app_model.app


class SiteMirror(object):
    """
    Class for site object used in request
    Instance contains site and Site User details
    """
    def __init__(self, request, *args, **kwargs):
        self.exists = False
        self.requested_app = self.get_requested_app(request)
        if not self.requested_app:
            return
        site = self.requested_app.site
        self.exists = True
        self.id = site.id
        self.name = site.name
        self.template_dir = site.template_dir
        self.site_user = SiteUserMirror(request, site)
        self.apps = self.get_site_apps()
        #self.requested_app =

    def get_requested_app(self, request):
        domain_name = request.META["HTTP_HOST"].split(":")[0]
        if 'www.' in domain_name:
            domain_name = domain_name.replace('www.', '')
        #TODO: implement cache here
        try:
            app = App.objects.get(domain_name=domain_name)
        except App.DoesNotExist:
            return None

        self.requested_app = AppMirror(app)
        return

    def get_site(self, request):
    #TODO: Implement cache layer.
        try:
            domain_name = request.META["HTTP_HOST"].split(":")[0]
            if 'www.' in domain_name:
                domain_name = domain_name.replace('www.', '')
            self.requested_domain_name = domain_name
            app_obj = App.objects.get(domain_name=domain_name)
            return app_obj.site
        except Site.DoesNotExist:
            return None

    def get_site_apps(self):
    #TODO: Implement cache layer.
        site_apps = App.objects.filter(site_id=self.id)
        apps = {}
        for each_app in site_apps:
            apps[each_app.app] = AppMirror(each_app)
        return apps

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


def core_home(request):
    return render_template(request, 'index.html',
                           app=settings.APPS['CORE'])


def cms_home(request):
    #TODO: render home template and content based on cms settings
    return render_template(request, 'index.html',
                           app=settings.APPS['CMS'])


def store_home(request):
    #TODO: render home template and content based on store settings
    return render_template(request, 'index.html',
                           app=settings.APPS['STORE'])


def blog_home(request):
    return render_template(request, 'index.html',
                           app=settings.APPS['BLOG'])


def support_home(request):
    return render_template(request, 'index.html',
                           app=settings.APPS['SUPPORT'])
