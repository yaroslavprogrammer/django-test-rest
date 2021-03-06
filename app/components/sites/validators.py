import requests

from django.core.exceptions import ValidationError

from .translation import gettext_lazy as _


class SiteAvailableValidator(object):
    """ Validate if site have 200 OK response"""

    def __call__(self, value):
        try:
            response = requests.get(value)
            response.raise_for_status()
        except:
            raise ValidationError(_('Site {} is not available').format(value))
