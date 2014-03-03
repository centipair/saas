from django.core.management.base import BaseCommand, CommandError
from core.models import Site
from django.contrib.auth.models import User
from django.conf import settings


def localhost_user():
    user, created = User.objects.get_or_create(username="admin",
                                               password="password")
    user.is_superuser = True
    user.is_staff = True
    user.save()
    if created:
        print "New user created"

    return user


def create_localhost():
    site, created = Site.objects.get_or_create(
        name='localhost',
        domain_name='localhost',
        service_domain_name='sub',
        template_name='default',
        template_dir='default',
        user=localhost_user(),
        default_app=settings.APPS['CORE']
    )
    if created:
        print "Localhost created"
    site.save()


class Command(BaseCommand):
    args = ''
    help = 'Creates new site for localhost devlelopment'

    def handle(self, *args, **options):
        try:
            create_localhost()
        except:
            raise CommandError('Command Error')

        self.stdout.write('Created new site for development')
