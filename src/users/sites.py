from django_otp.admin import OTPAdminSite

from users.forms import CustomOTPAuthenticationForm


class CustomOTPAdminSite(OTPAdminSite):
    """Customized admin site."""

    login_form = CustomOTPAuthenticationForm

    site_header = "Бот фонда 'Расправь крылья!'"
    site_title = "Бот фонда 'Расправь крылья!'"

    login_template = "authentication/login.html"
