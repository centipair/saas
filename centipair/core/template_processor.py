from django.shortcuts import render
from django.conf import settings
from centipair.core.models import App


def cdn_file(request, source):
    site = request.site
    template_path = site.template_dir + "/cdn/" + source
    source_file_url = settings.TEMPLATE_STATIC_URL + "/" + template_path
    return source_file_url


def core_cdn_file(request, source):
    source_file_url = settings.TEMPLATE_STATIC_URL + "/" +\
        settings.CORE_TEMPLATE_PATH + "/" + source
    return source_file_url


def get_base_path(request, base_file):
    site = request.site
    if site.is_core:
        base_path = settings.CORE_TEMPLATE_PATH + "/" +\
            site.template_dir + "/" + base_file
    else:
        base_path = site.template_dir + "/" + site.template_name + "/" +\
            base_file
    return base_path


def render_core_template(request, template_file, context):
    """Renders core templates """
    template_location = settings.CORE_TEMPLATE_PATH + "/" + template_file
    return render(request, template_location, context)


def render_cms_template(request, template_file, context):
    """Renders core templates """
    site = request.site
    template_dir = settings.CMS_TEMPLATE_PATH + "/" + site.template_name + "/"
    template_location = template_dir + template_file

    return render(request, template_location, context)


def render_template(request, template_file, context={}, app=None, base=None):
    """Renders template based on the site"""

    if app:
        if app == settings.APPS['CORE']:
            return render_core_template(request, template_file, context)
        else:
            return render_app_template(request, template_file, context,
                                       app, base)
    else:
        return render_core_template(request, "app_error.html", context)


def render_app_template(request, template_file, context, app, base):
    site = request.site
    app = App.objects.get(site_id=request.site.id, app=app)
    template_location = site.template_dir + "/" + app.template_dir +\
        "/" + app.template_name + "/" + template_file
    if context:
        context["centipair_base_template"] = base
    else:
        context = {}
        context["centipair_base_template"] = base

    return render(request, template_location, context)
