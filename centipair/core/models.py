from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    name = models.CharField(max_length=1024)
    domain_name = models.CharField(max_length=1024)
    service_domain_name = models.CharField(max_length=1024)
    template_name = models.CharField(max_length=1024)
    template_dir = models.CharField(max_length=1024)
    user = models.ForeignKey(User)
    default_app = models.CharField(max_length=128)
    is_core = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.name)


class Template(models.Model):
    name = models.CharField(max_length=1024)
    template_dir = models.CharField(max_length=1024)
    site = models.ForeignKey(Site)


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
