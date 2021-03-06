from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext as _
from centipair.core.models import Site, App, SiteUser
from centipair.core.utilities import generate_username


def create_site_user(username, user, site, role):
    site_user = SiteUser.objects.get_or_create(
        username=username,
        email=user.email,
        site=site,
        role=role,
        user=user
    )
    return site_user


def localhost_user():
    user, created = User.objects.get_or_create(
        username="admin",
        email=settings.ADMIN_EMAIL)
    user.set_password('password')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    if created:
        print (_("New admin user created"))

    return user


def create_core_app(site):
    app, created = App.objects.get_or_create(
        template_name='flat',
        template_dir='core',
        site=site,
        domain_name='localhost',
        app=settings.APPS['CORE'])

    site_admin_app, create = App.objects.get_or_create(
        domain_name='',
        template_name='admin',
        template_dir='site-admin',
        site=site,
        app=settings.APPS['SITE-ADMIN'])


def create_localhost():
    site, created = Site.objects.get_or_create(
        name='localhost',
        template_dir='centipair',
        default_app=settings.APPS['CORE'],
        domain_name='localhost',
        is_core=True
    )
    if created:
        print (_("Local site created"))
    create_core_app(site)
    site.save()
    user = localhost_user()
    create_site_user("admin", user, site, settings.SITE_ROLES['ADMIN'])
    return site


def create_store_app(site):
    cms_app, create = App.objects.get_or_create(
        domain_name=site.domain_name,
        subdomain_name='www',
        template_name='business-casual',
        template_dir='cms',
        site=site,
        app=settings.APPS['CMS'])
    cms_app.save()

    store_app, create = App.objects.get_or_create(
        domain_name='store.' + site.domain_name,
        subdomain_name='store',
        template_name='shop-homepage',
        template_dir='store',
        site=site,
        app=settings.APPS['STORE'])
    store_app.save()

    blog_app, create = App.objects.get_or_create(
        domain_name='blog.' + site.domain_name,
        subdomain_name='blog',
        template_name='blog-home',
        template_dir='blog',
        site=site,
        app=settings.APPS['BLOG'])
    blog_app.save()
    support_app, create = App.objects.get_or_create(
        domain_name='support.' + site.domain_name,
        subdomain_name='support',
        template_name='simple-sidebar',
        template_dir='support',
        site=site,
        app=settings.APPS['SUPPORT'])
    support_app.save()
    site_admin_app, create = App.objects.get_or_create(
        template_name='admin',
        template_dir='site-admin',
        site=site,
        app=settings.APPS['SITE-ADMIN'])


def store_user():
    user, created = User.objects.get_or_create(
        username=generate_username("seller"),
        email="devasiajosephtest@gmail.com")
    user.set_password('password')
    user.save()
    if created:
        print (_("New store user created"))

    return user


def create_test_store(core_site):
    site, created = Site.objects.get_or_create(
        name="my shop",
        default_app=settings.APPS['CMS'],
        template_dir='centipair-shop.com',
        domain_name='centipair-shop.com'
    )
    if created:
        print (_("New store created"))
    create_store_app(site)
    user = store_user()
    create_site_user("seller", user, site, settings.SITE_ROLES["ADMIN"])
    return


class Command(BaseCommand):
    args = ''
    help = _('Creates new site for localhost development')

    def handle(self, *args, **options):
        core_site = create_localhost()
        create_test_store(core_site)
        """
        try:
            create_localhost()
            create_test_store()
        except:
            raise CommandError(_('Command Error'))
        """
        self.stdout.write(_('Created new site for development'))
