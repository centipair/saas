from django.conf import settings
from django.http import HttpResponse
from centipair.core.views import AuthView
from centipair.core.template_processor import render_template
from django.db.models import get_model


class SiteAdminView(AuthView):
    """
    Core view for Site Admin
    """
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


class AdminHome(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "admin-base.html", app=self.app)


class Dashboard(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "dashboard.html", app=self.app)


class Sites(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Sites Loaded")


class MySites(OwnObjectsView):
    def get(self, request, *args, **kwargs):
        return


class SitePage(SiteAdminView):
    def get(self, request, site_id, *args, **kwargs):
        return HttpResponse("Sites" + str(site_id))
