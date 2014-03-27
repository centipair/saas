from centipair.core.views import SiteAdminView
from django.http import HttpResponse


class Dashboard(SiteAdminView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('This is dashboard')
