from django.shortcuts import render
from centipair.core.cache import get_site_app
from django.conf import settings


def cdn_file(request, source):
    """
    Returns cdn/static url for requested site
    """
    site = request.site
    file_path = site.template_dir + "/cdn/" + source
    source_file_url = settings.TEMPLATE_STATIC_URL + "/" + file_path
    return source_file_url


def core_cdn_file(request, source):
    """
    Returns cdn/static url for requested site admin
    """

    file_path = settings.CENTIPAIR_TEMPLATE_DIR + "/cdn/" + source
    source_file_url = settings.TEMPLATE_STATIC_URL + "/" + file_path
    return source_file_url


def render_template(request, template_file, context={}, app=None, base=None):
    """Renders template based on the site"""
    print context
    site = request.site
    site_template_dir = site.template_dir
    if app:
        app_obj = get_site_app(site.id, app)
        if app == settings.APPS['SITE-ADMIN'] or \
           app == settings.APPS['CORE']:
            site_template_dir = settings.CENTIPAIR_TEMPLATE_DIR
        else:
            site_template_dir = 'user-templates/' + site_template_dir
    else:
        app_obj = request.site.requested_app

    app_template_dir = app_obj.template_dir
    app_template_name = app_obj.template_name
    template_dir = site_template_dir + "/" + app_template_dir + "/" +\
        app_template_name + "/"
    template_location = template_dir + template_file

    if base:
        base_location = template_dir + base
        context["centipair_base_template"] = base_location
    print context
    return render(request, template_location, context)
