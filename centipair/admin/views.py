from django.conf import settings
from django.http import HttpResponse
from centipair.core.views import AuthView, FormView
from centipair.core.models import Site
from centipair.core.template_processor import render_template
from centipair.admin.serializers import SiteSerializer
from centipair.admin.forms import SiteForm
from django.db.models import get_model
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class SiteAdminView(AuthView):
    """
    Core view for Site Admin
    """
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']


class SiteAdminFormView(FormView):
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']


class OwnObjectsView(SiteAdminView):
    role = settings.SITE_ROLES['ADMIN']
    requested_object = 'Site'

    def has_site_permission(self, id):
        try:
            model = get_model('core', 'Site')
            model.objects.get(site_id=id, user=self.request.user)
        except model.DoesNotExist:
            return False

    def has_permission(self, id):
        if self.requested_object == 'Site':
            return self.has_site_permission(id)

    def dispatch(self, request, id, *args, **kwargs):
        if self.has_permission():
            return super(OwnObjectsView, self).dispatch(*args, **kwargs)
        else:
            return HttpResponse('Permission Denied', status=403)


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
        form = SiteForm()
        return render_template(request, "site_form.html",
                               app=self.app,
                               context={"form": form})


class SitesMineData(SiteAdminView):
    def get(self, request, *args, **kwargs):
        sites = Site.objects.filter(is_core=False,
                                    siteuser__user=request.user,
                                    siteuser__role=self.role)
        sites_serialized = SiteSerializer(sites, many=True)
        return JSONResponse(sites_serialized.data)
