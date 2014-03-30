from django.utils.translation import ugettext_lazy as _
from django import forms
from centipair.core.forms import AngularInput, SelectInput, SITE_APPS


class SiteForm(forms.Form):
    id = forms.IntegerField(widget=AngularInput(input_type="hidden"))
    name = forms.CharField(
        widget=AngularInput(label=_('Site name')))
    default_app = forms.CharField(widget=SelectInput(
        label="Default Application",
        options=SITE_APPS
    ))
    domain_name = forms.CharField(
        widget=AngularInput(label=_('Domain name')))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SiteForm, self).__init__(*args, **kwargs)
