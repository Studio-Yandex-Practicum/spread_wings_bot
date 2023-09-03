from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.sites import CustomOTPAdminSite

admin.site.__class__ = CustomOTPAdminSite

urlpatterns = [
    path("users/", include("users.urls"), name="users"),
    path("bot/", include("bot.urls"), name="bot"),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
admin.site.site_header = "Бот фонда 'Расправь крылья!'"
admin.site.site_title = "Бот фонда 'Расправь крылья!'"
