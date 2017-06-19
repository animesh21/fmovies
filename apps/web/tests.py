from django.test import TestCase
from .utility import ImdbHandler


class HelperMethodTests(TestCase):

    def test_str_to_percent(self):
        imdb = ImdbHandler()
        percent_str = '99.5%'
        percent = imdb.percent_to_float(percent_str)
        self.assertEqual(percent, 0.995)