from . import settings as base_settings
from .settings import *  # noqa: F403

SILENCED_SYSTEM_CHECKS = ['staticfiles.W004']

STORAGES = {
    **base_settings.STORAGES,
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
