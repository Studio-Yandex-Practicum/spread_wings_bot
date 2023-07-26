from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"), name="users"),
    path("bot/", include("bot.urls"), name="bot"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
