from django_otp.admin import OTPAdminSite

from users.forms import CustomOTPAuthenticationForm


class CustomOTPAdminSite(OTPAdminSite):
    """Customized admin site."""

    login_form = CustomOTPAuthenticationForm
    login_template = "authentication/login.html"
