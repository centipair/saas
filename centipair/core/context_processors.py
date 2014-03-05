from django.conf import settings


def template(context):
    if not hasattr(context, 'site'):
        return {
            "TEMPLATE_MEDIA_URL": "",
            "TEMPLATE_PATH": ""}
    site = context.site
    if site.is_core:
        template_media_url = settings.STATIC_URL + \
            "/templates/" + settings.CORE_TEMPLATE_PATH
    else:
        template_media_url = settings.MEDIA_URL + "templates/" + \
            site.template_dir + "/" + site.template_name + \
            "/resources/"
        template_path = site.template_dir+"/"+site.template_name
    return {
        "TEMPLATE_MEDIA_URL": template_media_url,
        "TEMPLATE_PATH": template_path}
