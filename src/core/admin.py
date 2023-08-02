from django.contrib import admin

from core.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):

    list_display = ("region_name", "region_key")
    list_filter = ("region_name", "region_key")
    search_fields = ("region_name", "region_key")
