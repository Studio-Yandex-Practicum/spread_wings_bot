from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User
from .utils import send_password_reset_email


class UserAdmin(BaseUserAdmin):
    """Custom user management via admin panel."""

    form = UserChangeForm
    add_form = UserCreationForm
    actions = ["reset_password"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "region",
        "is_staff",
        "role",
    )
    list_editable = ("role",)
    search_fields = ("first_name", "last_name", "email")
    ordering = ("region",)

    @admin.action(description="Сбросить пароль")
    def reset_password(self, request, queryset):
        """Send emails with password reset link to users."""
        for user in queryset:
            send_password_reset_email(user)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
