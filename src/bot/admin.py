from django.contrib import admin

from bot.models import Coordinator, FundProgram, Question


class RegionForAdmin(admin.ModelAdmin):
    def get_regions(self, instance):
        return [region.region_name for region in instance.regions.all()]

    get_regions.short_description = "Регионы"


@admin.register(Question)
class QuestionAdmin(RegionForAdmin):

    list_display = (
        "question",
        "answer",
        "short_description",
        "question_type",
        "get_regions",
    )
    list_filter = ("regions", "question_type")
    search_fields = (
        "question",
        "answer",
        "short_description",
        "question_type",
    )


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):

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

    list_display = ("title", "description", "get_regions")
    list_filter = ("regions",)
    search_fields = ("title", "description")
