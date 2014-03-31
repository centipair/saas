from django.conf import settings
import shutil


def initialize_template(dir_name):
    src = settings.STATIC_ROOT + '/templates/sample'
    dst = settings.STATIC_ROOT + '/templates/user-templates/'+dir_name
    shutil.copytree(src, dst)
    return
