from django.shortcuts import render
from django.conf import settings


def get_base_path(request, base_file):
    site = request.site
    if site.is_core:
        base_path = settings.CORE_TEMPLATE_PATH + "/" +\
            site.template_dir + "/" + base_file
    else:
        base_path = site.template_dir + "/" + site.template_name + "/" +\
            base_file
    return base_path


def render_core_template(request, template_file, context, base_file=None):
    """Renders core templates """
    site = request.site
    template_dir = settings.CORE_TEMPLATE_PATH + "/" + site.template_name + "/"
    template_location = template_dir + template_file
    if base_file:
        context["base"] = get_base_path(request, base_file)
    return render(request, template_location, context)


def render_cms_template(request, template_file, context):
    """Renders core templates """
    site = request.site
    template_dir = settings.CMS_TEMPLATE_PATH + "/" + site.template_name + "/"
    template_location = template_dir + template_file

    return render(request, template_location, context)


def render_template(request, template_file, context, app=None, base=None):
    """Renders template based on the site"""

    if app:
        if app == settings.APPS['CORE']:
            return render_core_template(request, template_file, context,
                                        base_file=base)
        elif app == settings.APPS['CMS']:
            return render_cms_template(request, template_file, context)
    site = request.site
    template_dir = site.template_dir + "/" + site.template_name + "/"
    template_location = template_dir + template_file
    if base:
        context["base"] = get_base_path(request, base)
    return render(request, template_location, context)


def render_app_template(request, template_file, context,
                        app=settings.APPS['CMS'],
                        base="base.html"):
    site = request.site
    app = App.objects.get(site=request.site, app=app)
    template = site.template_dir + "/" + app + "/" + app.template_name
