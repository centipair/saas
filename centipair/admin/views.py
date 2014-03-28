from django.conf import settings
from django.http import HttpResponse
from centipair.core.views import AuthView
from centipair.core.template_processor import render_template


class SiteAdminView(AuthView):
    """
    Core view for Site Admin
    """
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']


class AdminHome(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "admin-base.html", app=self.app)


class Dashboard(SiteAdminView):

    def get(self, request, *args, **kwargs):
        return render_template(request, "dashboard.html", app=self.app)


class Sites(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Sites Loaded")


class SitePage(SiteAdminView):
    def get(self, request, site_id, *args, **kwargs):
        return HttpResponse("Sites" + str(site_id))
