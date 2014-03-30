from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
# Create your tests here.


def logged_in_client(username="dev",
                     password="password"):
    c = Client()
    c.login(username=username, password=password)
    return c


def core_ajax_post(url_name, data, domain_name='localhost'):
    c = Client()
    response = c.post(reverse(url_name), data,
                      HTTP_HOST=domain_name,
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
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = get_page('login')
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        data = {"username": "user",
                "email": "testemail@domain.com",
                "password1": "password",
                "password2": "password",
                "tos": True}
        response = core_ajax_post('registration', data)
        self.assertEqual(response.status_code, 200)

    def test_login_email(self):
        # test login via email
        data = {"username": "devasiajosephtest@gmail.com",
                "password": "password"}

        response = core_ajax_post('login', data,
                                  domain_name='centipair-shop.com')

        response = core_ajax_post('login', data)
        self.assertEqual(response.status_code, 200)

    def test_login_username(self):
        # test login via username
        data = {"username": "seller",
                "password": "password"}
        response = core_ajax_post('login', data,
                                  domain_name='centipair-shop.com')

        response = core_ajax_post('login', data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
         # test invalid login
        data = {"username": "user1",
                "password": "password"}
        response = core_ajax_post('login', data)
        self.assertEqual(response.status_code, 422)
