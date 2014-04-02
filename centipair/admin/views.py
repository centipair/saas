from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
from django.db.models.loading import get_model
from centipair.core.views import AuthView, CoreFormView, JSONResponse
from centipair.core.models import Site, App
from centipair.core.template_processor import render_template
from centipair.admin.serializers import SiteSerializer, PageSerializer,\
    BlogSerializer
from centipair.admin.forms import SiteForm
from centipair.cms.forms import PageForm, BlogForm
from centipair.cms.models import Page


class SiteAdminView(AuthView):
    """
    Core view for Site Admin
    """
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']


class SiteAdminCRUD(CoreFormView):
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']
    login_required = True
    model = None
    context = {}
    list_template_name = ""
    serializer = None

    def get_action(self, request, *args, **kwargs):
        action = request.GET['action']
        if action == 'list':
            return self.get_list_view(request)
        elif action == 'list-data':
            return self.get_list_data(request)
        elif action == 'edit' or action == 'new':
            return self.render_form(request)

    def get_form_display(self, request):
        if 'id' in self.request.GET:
            try:
                form_object = self.model.objects.get(
                    pk=request.GET['id'],
                    site__siteuser__user=request.user,
                    site__siteuser__role=self.role
                )
            except self.model.DoesNotExist:
                return None
            form_init = self.form_class(initial=form_object.__dict__)
            return form_init
        else:
            form_init = self.form_class()
            return form_init

    def get_list_view(self, request):
        return render_template(request,
                               self.list_template_name,
                               app=self.app,
                               context=self.context)

    def get_list_data(self, request):
        sites = Site.objects.filter(is_core=False,
                                    siteuser__user=request.user,
                                    siteuser__role=self.role)
        objects = self.model.objects.filter(site__in=sites)
        serialized = self.serializer(objects, many=True)
        return JSONResponse(serialized.data)

    def render_form(self, request):
        form = self.get_form_display(request)
        if not form:
            return HttpResponse('Does Not Exists')
        self.context["form"] = form
        return render_template(request,
                               self.template_name,
                               app=self.app,
                               context=self.context)


class SiteAdminFormView(CoreFormView):
    role = settings.SITE_ROLES['ADMIN']
    app = settings.APPS['SITE-ADMIN']
    login_required = True
    form_model = None

    def get_form(self, request):
        if 'id' in self.request.GET:
            form_object = self.form_model.objects.get(
                pk=request.GET['id'],
                siteuser__user=request.user,
                siteuser__role=self.role
            )
            return form_object
            form = self.form_class(initial=form_object.__dict__)
            return form
        else:
            return self.form_class()

    def render_form(self, request, template, context={}):
        form = self.get_form(request)
        context["form"] = form
        return render_template(request,
                               template,
                               app=self.app,
                               context=context)


class Admin404(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Page Not Found')


class AdminHome(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "admin-base.html", app=self.app)


class Dashboard(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "dashboard.html", app=self.app)


class SitesPage(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return render_template(request, "sites.html", app=self.app)


class SitesEdit(SiteAdminFormView):
    form_class = SiteForm

    def get(self, request, id, *args, **kwargs):
        try:
            site = Site.objects.get(
                pk=id,
                is_core=False,
                siteuser__user=request.user,
                siteuser__role=self.role)
        except Site.DoesNotExist:
            return HttpResponse('Site not found', status=404)
        form = SiteForm(initial=site.__dict__)
        apps = App.objects.filter(site=site).exclude(
            app=settings.APPS['SITE-ADMIN'])
        return render_template(request, "site_form.html",
                               app=self.app,
                               context={"form": form, "apps": apps})

    def execute(self, form, request):
        return JSONResponse(form.save())


class AppEdit(SiteAdminFormView):
    def get(self, request, id, *args, **kwargs):
        #try:
        #except App.DoesNotExist:
        return render_template(request,
                               "app_form.html",
                               app=self.app,
                               context={})

    def execute(self, form, request):
        return


class SitesMineData(SiteAdminView):
    def get(self, request, *args, **kwargs):
        sites = Site.objects.filter(is_core=False,
                                    siteuser__user=request.user,
                                    siteuser__role=self.role)
        sites_serialized = SiteSerializer(sites, many=True)
        return JSONResponse(sites_serialized.data)


class Templates(SiteAdminView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Templates')


class PageEditView(SiteAdminCRUD):
    form_class = PageForm
    list_template_name = "page_list.html"
    template_name = "page_form.html"
    serializer = PageSerializer
    model = Page

    def get(self, request, *args, **kwargs):
        return self.get_action(request)

    def execute(self, request, form):
        return HttpResponse('form saved')


class BlogEditView(SiteAdminCRUD):
    form_class = BlogForm
    list_template_name = "blog_list.html"
    template_name = "blog_form.html"
    serializer = BlogSerializer
    model = Page

    def get(self, request, *args, **kwargs):
        return self.get_action(request)

    def execute(self, request, form):
        return HttpResponse('form saved')
