from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from centipair.core.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext as _


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


def create_localhost():
    site, created = Site.objects.get_or_create(
        name='localhost',
        domain_name='localhost',
        service_domain_name='sub',
        template_name='default',
        template_dir='default',
        user=localhost_user(),
        default_app=settings.APPS['CORE'],
        is_core=True
    )
    if created:
        print (_("Local site created"))
    site.save()


class Command(BaseCommand):
    args = ''
    help = _('Creates new site for localhost development')

    def handle(self, *args, **options):
        try:
            create_localhost()
        except:
            raise CommandError(_('Command Error'))

        self.stdout.write(_('Created new site for development'))
