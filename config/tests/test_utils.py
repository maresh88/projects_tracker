import os
import json

from test_plus.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from config.utils import get_secret_data


class TestUtils(TestCase):

    def test_get_secret_data_raise_error(self):
        data = dict()
        data['test_key'] = 'test_value'

        with open('test.json', 'w') as f:
            json.dump(data, f)

        with open('test.json', 'r') as f:
            secrets = json.loads(f.read())

        with self.assertRaises(ImproperlyConfigured) as context:
            get_secret_data('non_existent_value')

        self.assertEqual('Set the non_existent_value secret variable', str(context.exception))
