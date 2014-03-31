from django.utils.translation import ugettext_lazy as _
from django import forms
from centipair.core.forms import AngularInput, SelectInput, ObjectForm
from centipair.core.site import SITE_APPS


class SiteForm(ObjectForm):
    name = forms.CharField(
        widget=AngularInput(label=_('Site name')))
    default_app = forms.CharField(widget=SelectInput(
        label=_("Default Application"),
        options=SITE_APPS
    ))
    domain_name = forms.CharField(
        widget=AngularInput(label=_('Domain name')))

    def clean_domain_name(self):
        return self.cleaned_data['domain_name']

    def create(self):
        return {"message": _("Saved")}

    def update(self):
        return {"message": _("Updated")}

    #def clean_domain_name(self):

ACTIVE_OPTIONS = [
    {'name': 'Active', 'value': 1},
    {'name': 'Inactive', 'value': 0}]


class AppForm(ObjectForm):
    site_id = forms.IntegerField(
        widget=AngularInput(input_type='hidden'))
    domain_name = forms.CharField(
        widget=AngularInput(label=_('Domain name')))
    is_active = forms.IntegerField(
        widget=SelectInput(label=_('Status'), options=ACTIVE_OPTIONS))
