from centipair.core.models import Site, SiteUser, App


def to_dict(obj):
    dict_obj = obj.__dict__
    if '_state' in dict_obj:
        del dict_obj['_state']
    return dict_obj


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
