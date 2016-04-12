from django.contrib import admin

from .models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('url', 'is_private')
    list_filter = ('is_private',)
