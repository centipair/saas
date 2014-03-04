from django.shortcuts import render


def render_template(request, template_file, context):
    site = request.site
    template_dir = site.template_dir + "/" + site.template_name + "/"
    template_location = template_dir + template_file

    return render(request, template_location, context)
