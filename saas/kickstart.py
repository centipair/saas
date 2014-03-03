from django.core.management import setup_environ
import settings
setup_environ(settings)
from store.models import *
from core.models import *
import sys
import os
from django.contrib.auth.models import User


def save_categories():
    path = os.path.abspath(os.path.dirname(__file__))
    f = open(path + "/resources/categories", "r")
    store = Store.objects.all()[0]
    for category in f.readlines():
        c, created = ItemCategory.objects.get_or_create(
            name=category.replace("\n", ""),
            store=store)
        c.save()


def create_status():
    status = ["pending", "approved", "rejected", "signedup"]
    for each_status in status:
        status_obj = RequestStatus.objects.create(name=each_status)
        status_obj.save()


def initialize_site():
    user = User.objects.create(username="dev")
    user.set_password("password")
    user.is_superuser = True
    user.is_staff = True
    user.save()
    site = Site.objects.create(
        name="SomethingLocal",
        domain_name="somethingloc.al",
        template_name="default",
        template_dir=settings.CORE_TEMPLATE,
        user=user
    )
    site.save()


def main():
    if len(sys.argv) < 2:
        sys.exit("Must provide an option")
    else:
        if sys.argv[1] == 'setup':
            setup()
        elif sys.argv[1] == 'dev-setup':
            dev_setup()

if __name__ == '__main__':
    main()
