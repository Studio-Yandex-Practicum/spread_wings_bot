from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.plugins.otp_email.models import EmailDevice

from users.models import User
from users.utils.users.registration import generate_random_password


class UserCreationForm(forms.ModelForm):
    """A form for creating new users with random password."""

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def save(self, commit=True):
        """Save new user to db with random password."""
        user = super().save(commit=False)
        user.password = make_password(generate_random_password())
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
        )


class CustomOTPAuthenticationFormMixin(OTPAuthenticationFormMixin):
    """Customized OTPAuthenticationFormMixin mixin."""

    otp_error_messages = {
        "token_required": _("Пожалуйста, введите одноразовый код."),
        "challenge_exception": _("Ошибка генерации кода: {0}"),
        "not_interactive": _("Код не может быть отправлен."),
        "challenge_message": _("Код отправлен на указанную почту."),
        "invalid_token": _("Неверный код. Проверьте правильность."),
        "n_failed_attempts": ngettext_lazy(
            "Допущено %(failure_count) ошибок. Доступ временно ограничен.",
            "Допущено %(failure_count) ошибок. Доступ временно ограничен.",
            "failure_count",
        ),
        "verification_not_allowed": _("Верификация недоступна"),
    }

    def clean_otp(self, user):
        """Perform OTP clean."""
        if user is None:
            return

        validation_error = None
        with transaction.atomic():
            try:
                device = self._chosen_device(user)
                token = self.cleaned_data.get("otp_token")

                user.otp_device = None

                try:
                    if self.cleaned_data.get("otp_challenge"):
                        self._handle_challenge(device)
                    elif token:
                        user.otp_device = self._verify_token(
                            user, token, device
                        )
                    else:
                        self._handle_challenge(device)
                        raise forms.ValidationError(
                            self.otp_error_messages["token_required"],
                            code="token_required",
                        )
                finally:
                    if user.otp_device is None:
                        self._update_form(user)
            except forms.ValidationError as e:
                # Validation errors shouldn't abort the transaction, so we have
                # to carefully transport them out.
                validation_error = e

        if validation_error:
            raise validation_error

    def _chosen_device(self, user):
        """Return EmailDevise as default."""
        return EmailDevice.objects.filter(user=user).first()


class CustomOTPAuthenticationForm(
    CustomOTPAuthenticationFormMixin, AuthenticationForm
):
    """Customized OTPAuthenticationForm form."""

    otp_token = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"autocomplete": "off"})
    )

    otp_challenge = forms.CharField(required=False)

    def clean(self):
        """Clean form data."""
        self.cleaned_data = super().clean()
        self.clean_otp(self.get_user())

        return self.cleaned_data
