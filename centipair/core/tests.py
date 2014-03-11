from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
# Create your tests here.


def logged_in_client(username="dev",
                     password="password"):
    c = Client()
    c.login(username=username, password=password)
    return c


def core_ajax_post(url_name, data):
    c = Client()
    response = c.post(reverse(url_name), data,
                      HTTP_HOST='localhost',
                      HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    return response


def get_page(url_name):
    c = Client()
    response = c.get(reverse(url_name), HTTP_HOST='localhost')
    return response


class RegistrationTest(TestCase):
    fixtures = ['test_data.json']

    def test_registration_page(self):
        response = get_page('registration')
        print response.content

    def test_registration(self):
        data = {"username": "user",
                "email": "devasiajosephtest@gmai",
                "password1": "password",
                "password2": "password",
                "tos": True}
        response = core_ajax_post('registration', data)
        print response.content
        print response.status_code
