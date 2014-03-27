from django.conf import settings
from centipair.core.views import AuthView
from centipair.core.template_processor import render_template


class SiteAdminView(AuthView):
    """
    Core view for Site Admin
    """
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']


class Dashboard(SiteAdminView):

    def get(self, request, *args, **kwargs):
        return render_template(request, "index.html", app=self.app)


# Create your views here.
