from django.utils.translation import ugettext_lazy as _
from django import forms
from centipair.core.forms import AngularInput, SelectInput, SITE_APPS,\
    ObjectForm


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
