from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.conf import settings
from centipair.core.template_processor import render_template


def core_home(request):
    return render_template(request, 'index.html', None,
                           app=settings.APPS['CORE'])


def cms_home(request):
    #TODO: render home template and content based on cms settings
    return render_template(request, 'index.html', None,
                           app=settings.APPS['CMS'])


def user_site_home(request):
    if request.site.default_app == settings.APPS['cms']:
        return cms_home(request)
    else:
        #TODO: render a nice template
        return HttpResponse('App not found', status=404)


def home(request):
    if request.site.is_core:
        return core_home(request)
    else:
        return user_site_home(request)
    return HttpResponse(_('Hello world'))
