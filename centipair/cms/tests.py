from django.test import TestCase
from centipair.core.tests import logged_in_client, core_ajax_post, get_page 


class PostTest(TestCase):
    fixtures = ['test_data.json']


class PageTest(TestCase):
    fixtures = ['test_data.json']
