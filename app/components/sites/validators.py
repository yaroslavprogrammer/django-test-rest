import requests

from django.core.exceptions import ValidationError
from django.conf import settings

from .translation import gettext_lazy as _

if settings.DEBUG:
    import requests_cache

    requests_cache.install_cache('requests')


class SiteAvailableValidator(object):
    """ Validate if site have 200 OK response with given timeout """

    def __init__(self, timeout=5):
        self.timeout = timeout

    def __call__(self, value):
        try:
            response = requests.get(value)
            response.raise_for_status()
        except:
            raise ValidationError(_('Site {} is not available').format(value))
