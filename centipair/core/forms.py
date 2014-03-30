from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import EmailField
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.db import transaction
from PIL import Image, ImageOps
import os
from centipair.core.utilities import unique_name, generate_username, \
    generate_service_domain_name
from centipair.core.models import Site, SiteUser, App


SITE_APPS = [
    {'name': 'Website', 'value': 'cms'},
    {'name': 'Store', 'value': 'store'},
    {'name': 'Blog', 'value': 'blog'},
    {'name': 'Support Forum', 'value': 'support'}]


class SelectInput(forms.Widget):
    def __init__(self, *args, **kwargs):
        self.ng_init = ""
        if "label" in kwargs:
            self.label = kwargs.pop("label")
        else:
            self.label = ""
        if "options" in kwargs:
            self.options = kwargs.pop("options")
        else:
            self.options = []

        super(SelectInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value:
            self.ng_init = 'ng-init="form.%s=\'%s\'"' % (name, value)

        return render_to_string(
            'widgets/select.html',
            {"options": self.options,
             "name": name, "label": self.label,
             "ng_init": self.ng_init})


class AngularInput(forms.Widget):
    def __init__(self, *args, **kwargs):
        """A widget that can be used as AngularJs web input

        kwargs:
        label -- label for the input
        input_type -- type of input (text, checkbox, password..etc)
        default input type is text
        placeholder -- html place holder value
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


class ObjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.new = False
        super(ObjectForm, self).__init__(*args, **kwargs)

    id = forms.IntegerField(widget=AngularInput(input_type="hidden"))

    def save(self):
        if self.cleaned_data['id'] == 0:
            self.new = True
        if self.cleaned_data["id"] == u'':
            self.new = True
        if not self.cleaned_data["id"]:
            self.new = True

        if self.new:
            return self.create()
        else:
            return self.update()

    def create(self):
        return {'message': 'nothing created'}

    def update(self):
        return {'message': 'nothing updated'}


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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        site = Site.objects.get(pk=self.request.site.id)
        existing = SiteUser.objects.filter(
            username__iexact=self.cleaned_data['username'],
            site=site
        )

        if existing.exists():
            raise forms.ValidationError(
                _("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        site = Site.objects.get(pk=self.request.site.id)
        existing = SiteUser.objects.filter(
            email__iexact=self.cleaned_data['email'],
            site=site
        )
        if existing.exists():
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address."))
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'password1' in self.cleaned_data and 'password2' in \
           self.cleaned_data:
            if self.cleaned_data['password1'] != self.\
               cleaned_data['password2']:
                self._errors["password2"] = ErrorList(
                    [u"The two password fields didn't match."])
                raise forms.ValidationError(
                    _("The two password fields didn't match."))
        return self.cleaned_data

    def register(self):
        with transaction.atomic():
            generated_username = generate_username(
                self.cleaned_data["username"])
            user = User.objects.create(
                username=generated_username,
                email=self.cleaned_data["email"],
                is_active=True
            )
            user.set_password(self.cleaned_data["password1"])
            user.save()
            service_domain_name = generate_service_domain_name(user.username)
            site = Site(
                name="My Site",
                template_dir=user.username,
                default_app=settings.APPS['CMS'],
                active=True,
                domain_name=service_domain_name + "." +
                settings.CORE_DOMAIN_NAME
            )
            site.save()
            core_site_user = SiteUser(
                username=self.cleaned_data["username"],
                email=user.email,
                site_id=self.request.site.id,
                role=settings.SITE_ROLES['USER'],
                user=user,
                core_activation_code=unique_name(user.username)
            )
            core_site_user.save()
            site_user = SiteUser(
                username=self.cleaned_data["username"],
                email=user.email,
                site=site,
                role=settings.SITE_ROLES['ADMIN'],
                user=user
            )
            site_user.save()
            cms_app = App(
                template_name='default',
                template_dir='cms',
                site=site,
                app=settings.APPS['CMS'],
                domain_name=service_domain_name)
            cms_app.save()
        return


class AccountActivationForm(forms.Form):
    activation_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AccountActivationForm, self).__init__(*args, **kwargs)


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=AngularInput(label=_("Username"),
                            placeholder=_("Username")),
        max_length=30,
        label=_("Username"))

    password = forms.CharField(widget=AngularInput(
        label=_("Password"),
        placeholder=_("Password"),
        input_type="password"
    ))

    def clean(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data["username"]
        else:
            raise forms.ValidationError(_("Username and Password required"))
        if 'password' in self.cleaned_data:
            password = self.cleaned_data["password"]
        else:
            raise forms.ValidationError(_("Username and Password required"))
        try:
            # User can login via email address too
            # Check whether the provided username is email
            email_check = EmailField()
            email = email_check.clean(username)
            site_user = SiteUser.objects.get(email=email,
                                             site_id=self.request.site.id)
            unique_username = site_user.user.username
        except SiteUser.DoesNotExist:
            # Email does not exist in the current site
            raise forms.ValidationError(_("Username or password incorrect"))
        except forms.ValidationError:
            # Not an email. Probably user is trying to login via username
            try:
                site_user = SiteUser.objects.get(username=username,
                                                 site_id=self.request.site.id)
                unique_username = site_user.user.username
            except SiteUser.DoesNotExist:
                #User name does not exist in current database
                raise forms.ValidationError(
                    _("Username or password incorrect"))
        user = authenticate(username=unique_username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
            else:
                raise forms.ValidationError(
                    _("This account is deactivated."))
        else:
            raise forms.ValidationError(
                _("Username or password incorrect"))
