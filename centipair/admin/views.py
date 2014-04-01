from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
from centipair.core.views import AuthView, CoreFormView, JSONResponse
from centipair.core.models import Site, App
from centipair.core.template_processor import render_template
from centipair.admin.serializers import SiteSerializer
from centipair.admin.forms import SiteForm


class SiteAdminView(AuthView):
    """
    Core view for Site Admin
    """
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']


class SiteAdminFormView(CoreFormView):
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']
    login_required = True


class Admin404(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Page Not Found')


class AdminHome(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "admin-base.html", app=self.app)


class Dashboard(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "dashboard.html", app=self.app)


class SitesPage(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "sites.html", app=self.app)


class SitesEdit(SiteAdminFormView):
    form_class = SiteForm

    def get(self, request, id, *args, **kwargs):
        try:
            site = Site.objects.get(
                pk=id,
                is_core=False,
                siteuser__user=request.user,
                siteuser__role=self.role)
        except Site.DoesNotExist:
            return HttpResponse('Site not found', status=404)
        form = SiteForm(initial=site.__dict__)
        apps = App.objects.filter(site=site).exclude(
            app=settings.APPS['SITE-ADMIN'])
        return render_template(request, "site_form.html",
                               app=self.app,
                               context={"form": form, "apps": apps})

    def execute(self, form, request):
        return JSONResponse(form.save())


class AppEdit(SiteAdminFormView):
    def get(self, request, id, *args, **kwargs):
        #try:
        #except App.DoesNotExist:
        return render_template(request,
                               "app_form.html",
                               app=self.app,
                               context={})

    def execute(self, form, request):
        return


class SitesMineData(SiteAdminView):
    def get(self, request, *args, **kwargs):
        sites = Site.objects.filter(is_core=False,
                                    siteuser__user=request.user,
                                    siteuser__role=self.role)
        sites_serialized = SiteSerializer(sites, many=True)
        return JSONResponse(sites_serialized.data)


class Templates(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Templates')


class Pages(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Pages')
