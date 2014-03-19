from __future__ import with_statement
from fabric.api import local
import os
from fabric.api import *
from fabric.contrib.console import confirm

all_apps = ["centipair.core"]


def app_path(app):
    return app.replace('.', '/')


def manage(command):
    local('python manage.py ' + command)


def create_test_fixture(app):
    local('rm -f ' + app_path(app) + '/fixtures/test_data.json')
    local('python manage.py  dumpdata -e contenttypes >' + app_path(app) +
          '/fixtures/test_data.json --format=json')


def create_fixture(app):
    if app == "all":
        for each_app in all_apps:
            create_test_fixture(each_app)
    else:
        create_test_fixture(app)
