import os
import json

from django.core.exceptions import ImproperlyConfigured

with open(os.path.join(os.path.dirname(__file__), 'secrets.json'), 'r') as f:
    secrets = json.loads(f.read())


def get_secret_data(setting):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f'Set the {setting} secret variable'
        raise ImproperlyConfigured(error_msg)