from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from PIL import Image, ImageOps
import os
from centipair.core.utilities import unique_name


class AngularInput(forms.Widget):
    def __init__(self, *args, **kwargs):
        """A widget that displays JSON Key Value Pairs
        as a list of text input box pairs

        kwargs:
        key_attrs -- html attributes applied to the 1st input box pairs
        val_attrs -- html attributes applied to the 2nd input box pairs

        """

        self.label = ""
        self.input_type = "text"
        self.placeholder = ""
        if "label" in kwargs:
            self.label = kwargs.pop("label")
        if "input_type" in kwargs:
            self.input_type = kwargs.pop("input_type")
        if "placeholder" in kwargs:
            self.placeholder = kwargs.pop("placeholder")
        self.ng_init = ""

        super(AngularInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value:
            self.ng_init = "ng-init=\"form.%s='%s'\"" % (name, value)
        template = '<div class="form-group [{errors.%(name)sClass}]" ><label for="%(name)s">%(label)s</label><input type="%(input_type)s" class="form-control" id="%(name)s" placeholder="%(placeholder)s" ng-model="form.%(name)s" %(ng_init)s><label class="control-label">[{errors.%(name)s}]</label></div>' % {"label": self.label, "placeholder": self.placeholder, "input_type": self.input_type, "name": name, "ng_init": self.ng_init}
        return mark_safe(template)


class ImageForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ImageForm, self).__init__(*args, **kwargs)

    def get_thumb_filename(self, filename):
        return settings.UPLOAD_PATH + "thumb_" + filename

    def format_image(self, filename, width, prefix):
        format_image_name = settings.UPLOAD_PATH + prefix + "_" + filename
        image = Image.open(settings.UPLOAD_PATH + filename)
        size = image.size
        prop = width / float(image.size[0])
        if int(prop * float(image.size[1])) > 600:
            prop = width / float(image.size[1])

        size = (int(prop * float(image.size[0])),
                int(prop * float(image.size[1])))
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(format_image_name, 'JPEG')
        return prefix + "_" + filename

    def crop_format_image(self, filename, width, height, prefix):
        format_image_name = settings.UPLOAD_PATH + prefix + "_" + filename
        image = Image.open(settings.UPLOAD_PATH + filename)
        THUMBNAIL_SIZE = (width, height)

        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        # scale and crop to thumbnail
        imagefit = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)
        imagefit.save(format_image_name, 'JPEG')
        return prefix + "_" + filename

    def handle_uploaded_file(self, upload):
        upload_ext = os.path.splitext(upload.name)[1]
        generated_filename = unique_name(upload.name) + upload_ext
        upload_filename = settings.UPLOAD_PATH + generated_filename
        out = open(upload_filename, 'wb+')
        for chunk in upload.chunks():
            out.write(chunk)
        out.close()
        return generated_filename

    def delete_file(self, filename, prefixes):
        #try:
        if True:
            os.remove(settings.UPLOAD_PATH + filename)
            for prefix in prefixes:
                os.remove(settings.UPLOAD_PATH + prefix + "_" + filename)
        #except:
        #    pass
        return


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'

    username = forms.RegexField(
        widget=AngularInput(label=_("Username"),
                            placeholder=_("Username")),
        regex=r'^[\w.@+-]+$',
        max_length=30,
        label=_("Username"),
        error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    email = forms.EmailField(widget=AngularInput(
        label=_("Email"),
        placeholder=_("Email")))
    password1 = forms.CharField(widget=AngularInput(
        label=_("Password"),
        placeholder=_("Password"),
        input_type="password"
    ))
    password2 = forms.CharField(widget=AngularInput(
        label=_("Confirm Password"),
        placeholder=_("Password again"),
        input_type="password"
    ))

    tos = forms.BooleanField(
        widget=AngularInput(
            label=_("I have read and agree to the Terms of Service"),
            input_type="checkbox"
        ),
        label=_(u'I have read and agree to the Terms of Service'),
        error_messages={'required': _("You must agree to the terms to register")})

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(
                _("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.

    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.

    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']

    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.

        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']
