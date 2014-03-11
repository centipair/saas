from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Site(models.Model):
    name = models.CharField(max_length=1024)
    user = models.ForeignKey(User)
    default_app = models.CharField(max_length=64, default=settings.APPS['CMS'])
    domain_name = models.CharField(max_length=1024)
    service_domain_name = models.CharField(max_length=1024)
    store_domain_name = models.CharField(max_length=1024,
                                         null=True, blank=True)
    blog_domain_name = models.CharField(max_length=1024,
                                        null=True, blank=True)
    support_domain_name = models.CharField(max_length=1024,
                                           null=True, blank=True)
    template_dir = models.CharField(max_length=1024)
    is_core = models.BooleanField(default=False)

    def is_editor(self, user):
        if SiteManager.objects.filter(
                user=user,
                role=settings.SITE_ROLES['EDITOR']).exists():
            return True
        else:
            return False

    def is_admin(self, user):
        if SiteManager.objects.filter(
                user=user,
                role=settings.SITE_ROLES['ADMIN']).exists():
            return True
        else:
            return False

    def __unicode__(self):
        return u'%s' % (self.name)


class SiteManager(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    role = models.CharField(max_length=64)


class App(models.Model):
    template_name = models.CharField(max_length=1024)
    template_dir = models.CharField(max_length=1024)
    site = models.ForeignKey(Site)
    app = models.CharField(max_length=64)


class Page(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    edited_date = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    editor = models.ForeignKey(User)
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return u'%s' % (self.name)
