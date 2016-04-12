from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator

from mtr.utils.models.mixins import CreatedAtUpdatedAtMixin

from .validators import SiteAvailableValidator
from .translation import gettext_lazy as _


class ValidateOnSaveMixin(object):
    # https://www.xormedia.com/django-model-validation-on-save/
    # weird, will be added to utils

    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        super(ValidateOnSaveMixin, self).save(
            force_insert, force_update, **kwargs)


@python_2_unicode_compatible
class Site(ValidateOnSaveMixin, CreatedAtUpdatedAtMixin):
    url = models.CharField(max_length=255, validators=[
        RegexValidator(r'^https://.+$'), SiteAvailableValidator()])
    is_private = models.BooleanField(_('is private'), default=False)

    class Meta(CreatedAtUpdatedAtMixin.Meta):
        verbose_name = _('site')
        verbose_name_plural = _('sites')

    def __str__(self):
        return '{} - Private: {}'.format(self.url, self.is_private)
