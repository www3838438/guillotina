from copy import deepcopy
from guillotina.auth.users import ROOT_USER_ID
from guillotina.utils import lazy_apply

import base64
import guillotina.patch  # noqa
import os


TESTING_PORT = 55001

TESTING_SETTINGS = {
    "applications": ["guillotina.test_package"],
    "databases": [
        {
            "db": {
                "storage": "DUMMY",
                "name": "guillotina"
            }
        },
    ],
    "port": TESTING_PORT,
    "static": {
        "static": os.path.dirname(os.path.realpath(__file__)),
        "module_static": 'guillotina:',
        'favicon.ico': os.path.join(os.path.dirname(os.path.realpath(__file__)), '__init__.py')
    },
    "jsapps": {
        "jsapp_static": os.path.dirname(os.path.realpath(__file__)) + '/tests'
    },
    "default_static_filenames": ['teststatic.txt'],
    "creator": {
        "admin": "admin",
        "password": "admin"
    },
    "cors": {
        "allow_origin": ["*"],
        "allow_methods": ["GET", "POST", "DELETE", "HEAD", "PATCH"],
        "allow_headers": ["*"],
        "expose_headers": ["*"],
        "allow_credentials": True,
        "max_age": 3660
    },
    "root_user": {
        "password": "admin"
    },
    "jwt": {
        "secret": "foobar",
        "algorithm": "HS256"
    },
    "utilities": [],
    "logging": {
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            'foobar': {
                'handlers': [],
                'level': 'INFO',
                'propagate': True
            }
        }
    },
    'pg_connection_class': 'guillotina.db.storages.pg.LightweightConnection'
}


QUEUE_UTILITY_CONFIG = {
    "provides": "guillotina.async_util.IQueueUtility",
    "factory": "guillotina.async_util.QueueUtility",
    "settings": {}
}


ADMIN_TOKEN = base64.b64encode(
    '{}:{}'.format(ROOT_USER_ID, TESTING_SETTINGS['root_user']['password']).encode(
        'utf-8')).decode('utf-8')
DEBUG = False


_configurators = []


def configure_with(func):
    _configurators.append(func)


def get_settings(override_settings={}):
    settings = deepcopy(TESTING_SETTINGS)
    for func in _configurators:
        lazy_apply(func, settings, _configurators)
    return settings
