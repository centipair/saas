from django.shortcuts import render
from centipair.core.cache import get_site_app


def render_template_new(request, template_file,
                        context={}, app=None, base=None):
    """Renders template based on the site"""

    site = request.site
    site_template_dir = site.template_dir
    if app:
        app_obj = get_site_app(site.id, app)
    else:
        app_obj = request.site.requested_app

    app_template_dir = app_obj.template_dir
    app_template_name = app_obj.template_name
    template_dir = site_template_dir + "/" + app_template_dir + "/" +\
        app_template_name + "/"
    template_location = template_dir + template_file
    base_location = template_dir + base

    if base:
        context["centipair_base_template"] = base_location

    return render(request, template_location, context)
