from django.contrib import admin

from bot.forms import QuestionAdminForm
from bot.models import Coordinator, FundProgram, ProxyRegion, Question


class RegionForAdmin(admin.ModelAdmin):
    """Base class; getting the list of regions."""

    def get_regions(self, instance):
        """List of region names (without region key)."""
        return [region.region_name for region in instance.regions.all()]

    get_regions.short_description = "Регионы"


@admin.register(Question)
class QuestionAdmin(RegionForAdmin):
    """Admin model for class Question."""

    form = QuestionAdminForm
    list_display = (
        "question",
        "short_description",
        "question_type",
        "get_answer",
        "get_regions",
    )
    list_filter = ("regions", "question_type")
    search_fields = (
        "question",
        "answer",
        "short_description",
        "question_type",
    )

    @admin.display(description="Ответ")
    def get_answer(self, obj):
        """Display responses in admin panel."""
        return obj.answer[:100]


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    """Admin model for class Coordinator."""

    list_display = (
        "first_name",
        "last_name",
        "region",
        "email_address",
        "phone_number",
        "telegram_account",
    )
    list_filter = ("region",)
    search_fields = (
        "first_name",
        "last_name",
        "email_address",
        "phone_number",
        "telegram_account",
    )


@admin.register(FundProgram)
class FundProgramAdmin(RegionForAdmin):
    """Admin model for class FundProgram."""

    list_display = ("title", "short_description", "fund_text", "get_regions")
    list_filter = ("regions",)
    search_fields = ("title", "short_description")


@admin.register(ProxyRegion)
class ProxyRegionAdmin(admin.ModelAdmin):
    """Admin model for class Region."""

    exclude = ["region_key"]
