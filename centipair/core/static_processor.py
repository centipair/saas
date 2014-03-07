from django.conf import settings


def cdn_file(request, source):
    site = request.site
    template_path = site.template_dir + "/" + site.template_name
    source_file_url = settings.TEMPLATE_STATIC_URL + template_path + source
    return source_file_url


def core_cdn_file(request, source):
    site = request.site
    template_path = settings.CORE_TEMPLATE_PATH + "/" + \
        site.template_name
    source_file_url = settings.TEMPLATE_STATIC_URL + "/" + template_path + \
        "/" + source
    return source_file_url
