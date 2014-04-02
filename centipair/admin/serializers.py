from rest_framework import serializers
from centipair.core.models import Site, SiteUser
from centipair.cms.models import Page


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('id', 'name', 'default_app', 'active', 'domain_name')


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'title', 'url', 'description',
                  'meta_description', 'meta_keywords',
                  'site')
