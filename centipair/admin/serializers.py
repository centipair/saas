from rest_framework import serializers
from centipair.core.models import Site, SiteUser


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('id', 'name', 'default_app', 'active', 'domain_name')
