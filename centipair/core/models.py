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

    def __unicode__(self):
        return u'%s' % (self.name)


class SiteUser(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=1024)
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    role = models.CharField(max_length=64)
    core_activation_code = models.CharField(max_length=128,
                                            null=True, blank=True)
    site_activeation_code = models.CharField(max_length=128,
                                             null=True, blank=True)

    @property
    def is_admin(self):
        if self.role == settings.SITE_ROLES['ADMIN']:
            return True
        else:
            return False

    @property
    def is_editor(self):
        if self.role == settings.SITE_ROLES['EDITOR']:
            return True
        elif self.role == settings.SITE_ROLES['ADMIN']:
            return True
        else:
            return False


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
