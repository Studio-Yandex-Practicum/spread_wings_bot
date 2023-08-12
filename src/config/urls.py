from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"), name="users"),
    path("bot/", include("bot.urls"), name="bot"),
]

admin.site.site_header = "Бот фонда 'Расправь крылья'"
admin.site.site_title = "Бот фонда 'Расправь крылья'"
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
