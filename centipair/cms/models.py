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
    edited_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField()
    site = models.ForeignKey(Site)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.name)


class PageDraft(models.Model):
    page = models.OnToOneField(Page)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    edited_date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.page.title = self.title
        self.page.description = self.description
        self.page.url = self.url
        self.page.published = True
        self.page.save()
        #TODO: update edit history


class PageEditHistory(models.Model):
    page = models.OnToOneField(Page)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    editor = models.ForeignKey(User)
    edited_date = models.DateTimeField(auto_now_add=True)


class BlogPost(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    editor = models.ForeignKey(User)
    edited_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField()
    site = models.ForeignKey(Site)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.name)


class BlogPostDraft(models.Model):
    blog_post = models.OnToOneField(BlogPost)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    edited_date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.blog_post.title = self.title
        self.blog_post.description = self.description
        self.blog_post.url = self.url
        self.blog_post.published = True
        self.blog_post.save()
        #TODO: update blogpost edit history


class BlogPostEditHistory(models.Model):
    blog_post = models.OnToOneField(BlogPost)
    title = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024,
                                   blank=True,
                                   null=True)
    url = models.CharField(max_length=1024)
    meta_description = models.CharField(max_length=150,
                                        null=True,
                                        blank=True)
    editor = models.ForeignKey(User)
    edited_date = models.DateTimeField(auto_now_add=True)


class Template(models.Model):
    file_name = models.CharField(max_length=128)
    app = models.ForeignKey(App)
