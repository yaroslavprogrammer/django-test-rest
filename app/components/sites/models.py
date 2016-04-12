from django.db import models

from mtr.utils.models.mixins import CreatedAtUpdatedAtMixin

from .translation import gettext_lazy as _


class Site(CreatedAtUpdatedAtMixin):
    url = models.SlugField()
    is_private = models.BooleanField(_('is private'), default=False)

    class Meta(CreatedAtUpdatedAtMixin.Meta):
        verbose_name = _('site')
        verbose_name_plural = _('sites')

    def __str__(self):
        return '{} - Private: {}'.format(self.url, self.is_private)
