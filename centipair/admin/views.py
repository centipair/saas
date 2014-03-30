from django.conf import settings
from django.http import HttpResponse
from centipair.core.views import AuthView, CoreFormView, JSONResponse
from centipair.core.models import Site
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
        site = Site.objects.get(is_core=False,
                                siteuser__user=request.user,
                                siteuser__role=self.role)
        form = SiteForm(initial=site.__dict__)
        return render_template(request, "site_form.html",
                               app=self.app,
                               context={"form": form})

    def execute(self, form, request):
        return JSONResponse(form.save())


class SitesMineData(SiteAdminView):
    def get(self, request, *args, **kwargs):
        sites = Site.objects.filter(is_core=False,
                                    siteuser__user=request.user,
                                    siteuser__role=self.role)
        sites_serialized = SiteSerializer(sites, many=True)
        return JSONResponse(sites_serialized.data)
