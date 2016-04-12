from django.conf import settings
# from django.db import models

# from localeurl.sitemaps import LocaleurlSitemap

sitemaps = {}


def register(name, langs=True):
    def decorator(cls):
        if langs:
            for lang, lname in settings.LANGUAGES:
                sitemaps['{}-{}'.format(name, lang)] = cls(lang)
        else:
            sitemaps[name] = cls()
        return cls
    return decorator

# just for example

# @register('pages')
# class PagesSitemap(LocaleurlSitemap):
#     def items(self):
#         return Menu.objects.exclude(
#             models.Q(url='') & models.Q(page__url=''))
