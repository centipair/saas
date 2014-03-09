from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from centipair.core.template_processor import render_template
from centipair.core.static_processor import cdn_file, core_cdn_file


def core_home(request):
    return render_template(request, 'index.html', {},
                           app=settings.APPS['CORE'])


def cms_home(request):
    #TODO: render home template and content based on cms settings
    return render_template(request, 'index.html', {},
                           app=settings.APPS['CMS'])


def store_home(request):
    #TODO: render home template and content based on store settings
    return render_template(request, 'index.html', {},
                           app=settings.APPS['STORE'])


def user_site_home(request):
    if request.site.default_app == settings.APPS['cms']:
        return cms_home(request)
    elif request.site.default_app == settings.APPS['store']:
        return store_home(request)
    else:
        #TODO: render a nice template
        return HttpResponse('App not found', status=404)


def home(request):
    if request.site.is_core:
        return core_home(request)
    else:
        return user_site_home(request)
    return HttpResponse(_('Hello world'))


def core_pricing(request):
    return render_template(request, 'pricing.html', {},
                           app=settings.APPS['CORE'],
                           base="base.html")


def cdn_redirect(request, source):
    return redirect(cdn_file(request, source))


def core_cdn_redirect(request, source):
    return redirect(core_cdn_file(request, source))
