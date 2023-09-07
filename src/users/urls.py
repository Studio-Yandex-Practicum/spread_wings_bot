from django.urls import path

from users.views import PasswordSetView

app_name = "users"

urlpatterns = [
    path(
        "set_password/<uidb64>/<token>/",
        PasswordSetView.as_view(),
        name="password_set",
    ),
]
