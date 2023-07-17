from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BotUpdateView

urlpatterns = [
    path("webhook", csrf_exempt(BotUpdateView.as_view())),
]
