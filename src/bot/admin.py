from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db.models import TextField

from bot.forms import FundProgramForm, QuestionAdminForm
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
        "get_question",
        "get_short_description",
        "get_question_type",
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

    @admin.display(description="Вопрос")
    def get_question(self, obj):
        """Display questions in admin panel."""
        return obj.question[:100]

    @admin.display(description="Короткое описание")
    def get_short_description(self, obj):
        """Display short_descriptions in admin panel."""
        return obj.short_description[:100]

    @admin.display(description="Тип вопроса")
    def get_question_type(self, obj):
        """Display question_type in admin panel."""
        return obj.question_type[:100]

    @admin.display(description="Ответ")
    def get_answer(self, obj):
        """Display answer in admin panel."""
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

    form = FundProgramForm
    list_display = ("title", "short_description", "fund_text", "get_regions")
    formfield_overrides = {TextField: {"widget": CKEditorWidget}}
    list_filter = ("regions",)
    search_fields = ("title", "short_description")

    @admin.display(description="Название")
    def get_title(self, obj):
        """Display title in admin panel."""
        return obj.title[:100]

    @admin.display(description="Короткое описание")
    def get_short_description(self, obj):
        """Display short_description in admin panel."""
        return obj.short_description[:100]

    @admin.display(description="Описание программы")
    def get_fund_text(self, obj):
        """Display fund_text in admin panel."""
        return obj.fund_text[:100]


@admin.register(ProxyRegion)
class ProxyRegionAdmin(admin.ModelAdmin):
    """Admin model for class Region."""

    exclude = ["region_key"]
