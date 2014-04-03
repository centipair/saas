from centipair.core.models import Site
from django.conf import settings


def my_sites(user):
    sites = Site.objects.filter(
        is_core=False,
        siteuser__user=user,
        siteuser__role=settings.SITE_ROLES['ADMIN'])
    print sites
    return sites


def my_site_options(user):
    sites = my_sites(user)
    site_options = []
    for site in sites:
        site_option = {"name": site.name + "(" + site.domain_name + ")",
                       "value": site.id}
        site_options.append(site_option)
    return site_options


SITE_APPS = [
    {'name': 'Website', 'value': 'cms'},
    {'name': 'Store', 'value': 'store'},
    {'name': 'Blog', 'value': 'blog'},
    {'name': 'Support Forum', 'value': 'support'}]

SITE_APPS_REVERSE = {'cms': 'Website',
                     'store': 'Store',
                     'blog': 'Blog',
                     'support': 'Support Forum'}
