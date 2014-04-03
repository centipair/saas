from django.utils.translation import ugettext_lazy as _
from django import forms
from centipair.cms.models import Page
from centipair.core.forms import AngularInput, SelectInput, AngularTextArea,\
    ObjectForm, CkEditor


class PageForm(ObjectForm):
    site = forms.IntegerField(widget=SelectInput(label=_('Site')))
    title = forms.CharField(
        widget=AngularInput(label=_('Title')))
    url = forms.CharField(widget=AngularInput(label=_('URL')))
    description = forms.CharField(
        widget=CkEditor(label=_('Description')),
        required=False)
    meta_description = forms.CharField(
        widget=AngularInput(label=_('Meta Description')),
        required=False)
    meta_keywords = forms.CharField(
        widget=AngularInput(label=_('Meta Keywords')),
        required=False)


class BlogForm(ObjectForm):
    site = forms.IntegerField(widget=SelectInput(label=_('Site')))
    title = forms.CharField(
        widget=AngularInput(label=_('Title')))
    url = forms.CharField(widget=AngularInput(label=_('URL')))
    description = forms.CharField(
        widget=AngularTextArea(label=_('Description')),
        required=False)
    meta_description = forms.CharField(
        widget=AngularInput(label=_('Meta Description')),
        required=False)
    meta_keywords = forms.CharField(
        widget=AngularInput(label=_('Meta Keywords')),
        required=False)
