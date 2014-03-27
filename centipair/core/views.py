from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic.base import View
from centipair.core.forms import RegistrationForm, LoginForm
from centipair.core.template_processor import render_template, cdn_file
from centipair.core.cache import valid_site_role_cache
import json


def home(request):
    return render_template(request, "index.html", base="base.html")


def core_pricing(request):
    return render_template(request, 'pricing.html',
                           app=settings.APPS['CORE'],
                           base="base.html")


def cdn_redirect(request, source):
    return redirect(cdn_file(request, source))


def core_cdn_redirect(request, source):
    return redirect(cdn_file(request, source))


class CoreView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(CoreView, self).dispatch(request, *args, **kwargs)


class AuthView(CoreView):
    role = settings.SITE_ROLES['USER']
    app = None
    login_required = True

    def dispatch(self, request, *args, **kwargs):
        if self.app not in self.request.site.apps:
            return HttpResponse('app not found', status=404)
        if self.login_required:
            if request.user.is_authenticated():
                if valid_site_role_cache(request, self.role):
                    return super(CoreView, self).dispatch(request,
                                                          *args, **kwargs)
                else:
                    return HttpResponse('Permission Denied', status=403)
            else:
                return HttpResponse('Login required', status=403)
        else:
            return super(CoreView, self).dispatch(request, *args, **kwargs)


class SiteAdminView(AuthView):
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']


class CoreFormView(FormView):
    response_json = {}
    success_message = _("Success")
    system_error_message = _("System error.Please try again after sometime")
    form_error_message = _("Submitted data is invalid.")

    def dispatch(self, *args, **kwargs):
        if self.app not in self.request.site.apps:
            return HttpResponse('app not found', status=404)
        return super(CoreFormView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CoreFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        self.response_json["errors"] = form.errors
        self.response_json["message"] = self.form_error_message
        return self.render_to_json_response(self.response_json, status=422)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        try:
            return self.execute(form)
        except:
            self.response_json["status"] = 500
            self.response_json["message"] = self.system_error_message
            return self.render_to_json_response(self.response_json, status=500)
            #TODO: Log this error for future debugging

    def execute(self, form):
        """
        This method can be overridden in inherited Class
        Business logic can be put here.
        """
        return HttpResponse(_(self.success_message))


class RegistrationView(CoreFormView):
    form_class = RegistrationForm
    template_name = settings.CORE_TEMPLATE_PATH + '/registration_form.html'
    success_message = _("Registration success. Please activate your account by following the instructions we send to your email.")
    app = settings.APPS['CORE']

    def execute(self, form):
        form.register()
        return HttpResponse(_(self.success_message))

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render_template(request,
                               "registration_form.html",
                               context={"form": form},
                               app=settings.APPS['CORE'],
                               base="base.html")


class LoginView(CoreFormView):
    form_class = LoginForm
    template_name = settings.CORE_TEMPLATE_PATH + '/login_form.html'
    success_message = _("Login success")
    app = settings.APPS['CORE']

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render_template(request,
                               "login_form.html",
                               context={"form": form},
                               app=settings.APPS['CORE'],
                               base="base.html")

    def execute(self, form):
        return HttpResponse(_(self.success_message))
