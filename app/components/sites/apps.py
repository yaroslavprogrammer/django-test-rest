from django.apps import AppConfig as BaseAppConfig

from .translation import gettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'app.components.sites'
    verbose_name = _('Sites')
