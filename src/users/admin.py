from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

from utils.emailing.reset_password import send_password_reset_email

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    """Custom user management via admin panel."""

    form = UserChangeForm
    add_form = UserCreationForm
    actions = ["reset_password"]

    fieldsets = (
        (None, {"fields": ("email",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
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
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    list_display = (
        "get_fullname",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    search_fields = ("first_name", "last_name", "email")
    ordering = ("last_name",)

    list_filter = ("is_active",)

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    @admin.display(description="Имя и Фамилия")
    def get_fullname(self, obj):
        """Display fullname user in admin panel."""
        if not obj.first_name:
            return "User"
        return f"{obj.first_name} {obj.last_name}"

    @admin.action(description="Сбросить пароль")
    def reset_password(self, request, queryset):
        """Send emails with password reset link to users."""
        for user in queryset:
            send_password_reset_email(user)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


def permissions_new_unicode(self):
    """Translate default permissions."""
    class_name = str(self.content_type)
    permissions_name = str(self.name)

    if "Can delete" in permissions_name:
        permissions_name = "разрешено удалять"
    elif "Can add" in permissions_name:
        permissions_name = "разрешено добавлять"
    elif "Can change" in permissions_name:
        permissions_name = "разрешено изменять"
    elif "Can view" in permissions_name:
        permissions_name = "разрешено просматривать"

    return "%s - %s" % (class_name.title(), permissions_name)


Permission.__str__ = permissions_new_unicode
