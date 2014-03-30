from centipair.core.models import Site, App, SiteUser
from django.conf import settings


def to_dict(obj):
    dict_obj = obj.__dict__
    if '_state' in dict_obj:
        del dict_obj['_state']
    return dict_obj


class AppMirror(object):
    def __init__(self, app_dict, *args, **kwargs):
        self.template_name = app_dict["template_name"]
        self.template_dir = app_dict["template_dir"]
        self.app = app_dict["app"]
        self.domain_name = app_dict["domain_name"]
        self.site_id = app_dict["site_id"]


class SiteUserMirror(object):
    def __init__(self, user_dict, *args, **kwargs):
        if not user_dict:
            self.role = settings.SITE_ROLES['NONE']
        else:
            self.role = user_dict['role']
            self.username = user_dict['username']
            self.email = user_dict['email']
            self.user_id = user_dict['user_id']


def get_site_user_cache(request):
    if not request.user.is_authenticated():
        return SiteUserMirror(None)
    try:
        #TODO: implement cache if possible
        site_user = SiteUser.objects.get(user_id=request.user.id,
                                         site_id=request.site.id)
        site_user_mirror = SiteUserMirror(to_dict(site_user))
        return site_user_mirror

    except SiteUser.DoesNotExist:
        return None


def valid_site_role_cache(request, role):
    """
    Checks for appropriate site role
    """
    try:
        #TODO: implement cache here
        SiteUser.objects.get(user=request.user,
                             site_id=request.site.id,
                             role=role)
        return True
    except SiteUser.DoesNotExist:
        return False


def get_app_cache(domain_name):
    """
    Returns a dictionary fetched from cache
    """
    try:
        #TODO: fetch from cache
        app = App.objects.get(domain_name=domain_name)
        # mocking response map from cache
        app_dict = to_dict(app)
        return app_dict

    except App.DoesNotExist:
        return None


def get_site_app_cache(site_id, app):
    #TODO: implement cache if necessary
    app_obj = App.objects.get(site_id=site_id, app=app)
    # mocking response map from cache
    app_dict = to_dict(app_obj)
    return app_dict


def get_site_app(site_id, app):
    app_dict = get_site_app_cache(site_id, app)
    return AppMirror(app_dict)


def get_site_apps_cache(site_id):
    #TODO: implement cache here
    app_objects = App.objects.filter(site_id=site_id)
    apps = []
    for app in app_objects:
        apps.append(app.app)
    return apps


def get_site_cache(site_id):
    try:
        #TODO: fetch from cache
        site = Site.objects.get(pk=site_id)
        #mocking response map from cache
        site_dict = to_dict(site)
        return site_dict
    except Site.DoesNotExist:
        return None

    return
