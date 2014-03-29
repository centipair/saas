from django.utils.translation import ugettext_lazy as _
from django import forms
from centipair.core.forms import AngularInput, SelectInput


class SiteForm(forms.Form):
    name = forms.CharField(
        widget=AngularInput(label=_('Site name')))
    default_app = forms.ChoiceField(widget=SelectInput(label="Default Application"))
    domain_name = forms.CharField(
        widget=AngularInput(label=_('Domain name')))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SiteForm, self).__init__(*args, **kwargs)
