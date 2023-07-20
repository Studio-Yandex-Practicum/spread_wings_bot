from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User management via admin panel."""

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        # "region",
        "is_staff",
        "role",
    )
    # list_filter = ("region")
