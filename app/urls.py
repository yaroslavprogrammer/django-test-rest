from django.conf.urls import include, patterns, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# from .sitemaps import sitemaps


urlpatterns = i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
)

# i18n independent patterns

# urlpatterns += patterns(
#     '',
# )

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
