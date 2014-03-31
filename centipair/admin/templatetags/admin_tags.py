from django import template
from centipair.core.site import SITE_APPS_REVERSE

register = template.Library()


@register.filter
def active_label(value):
    if value:
        label = '<span class="label label-success">Active</span>'
    else:
        label = '<span class="label label-danger">Inactive</span>'

    return label


@register.filter
def app_name(value):
    if value in SITE_APPS_REVERSE:
        return SITE_APPS_REVERSE[value]
    else:
        return 'None'
    return
