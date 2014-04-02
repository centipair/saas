from django.db import models
from django.contrib.auth.models import User
from centipair.core.models import Site, App


class Page(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    meta_keywords = models.CharField(max_length=150,
                                     null=True, blank=True)
    edited_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField()
    site = models.ForeignKey(Site)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.name)


class PageDraft(models.Model):
    page = models.OneToOneField(Page)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    meta_keywords = models.CharField(max_length=150,
                                     null=True, blank=True)
    edited_date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.page.title = self.title
        self.page.description = self.description
        self.page.url = self.url
        self.page.meta_description = self.meta_description
        self.page.meta_keywords = self.meta_keywords
        self.page.published = True
        self.page.save()
        #TODO: update edit history


class PageEditHistory(models.Model):
    page = models.OneToOneField(Page)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    meta_keywords = models.CharField(max_length=150,
                                     null=True, blank=True)
    editor = models.ForeignKey(User)
    edited_date = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    meta_keywords = models.CharField(max_length=150,
                                     null=True, blank=True)
    editor = models.ForeignKey(User)
    edited_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField()
    site = models.ForeignKey(Site)
    published = models.BooleanField(default=False)
    featured_image = models.CharField(max_length=1028,
                                      null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)


class PostDraft(models.Model):
    post = models.OneToOneField(Post)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    meta_keywords = models.CharField(max_length=150,
                                     null=True, blank=True)
    edited_date = models.DateTimeField(auto_now_add=True)
    featured_image = models.CharField(max_length=128,
                                      null=True, blank=True)

    def publish(self):
        self.post.title = self.title
        self.post.description = self.description
        self.post.url = self.url
        self.post.meta_description = self.meta_description
        self.post.meta_keywords = self.meta_keywords
        self.post.published = True
        self.post.save()
        #TODO: update blogpost edit history


class PostEditHistory(models.Model):
    post = models.OneToOneField(Post)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    meta_keywords = models.CharField(max_length=150,
                                     null=True, blank=True)
    editor = models.ForeignKey(User)
    edited_date = models.DateTimeField(auto_now_add=True)
    featured_image = models.CharField(max_length=128,
                                      null=True, blank=True)


class Template(models.Model):
    file_name = models.CharField(max_length=128)
    app = models.ForeignKey(App)
