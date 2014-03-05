from django.shortcuts import render
from django.conf import settings


def render_core_template(request, template_file, context):
    """Renders core templates """
    site = request.site
    template_dir = settings.CORE_TEMPLATE_PATH + "/" + site.template_name + "/"
    template_location = template_dir + template_file
    print "herere"
    return render(request, template_location, context)


def render_cms_template(request, template_file, context):
    """Renders core templates """
    site = request.site
    template_dir = settings.CMS_TEMPLATE_PATH + "/" + site.template_name + "/"
    template_location = template_dir + template_file

    return render(request, template_location, context)


def render_template(request, template_file, context, app=None):
    """Renders template based on the site"""

    if app:
        if app == settings.APPS['CORE']:
            return render_core_template(request, template_file, context)
        elif app == settings.APPS['CMS']:
            return render_cms_template(request, template_file, context)
    site = request.site
    template_dir = site.template_dir + "/" + site.template_name + "/"
    template_location = template_dir + template_file

    return render(request, template_location, context)
