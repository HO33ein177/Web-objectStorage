import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


def validate_english_username(value):
    if not re.match(r'^[a-zA-Z]+$', value):
        raise ValidationError('Username must contain only English letters.')

    user = get_user_model()
    if user.objects.filter(username__iexact=value).exists():
        raise ValidationError('Username already exists.')


def custom_email_validator(value):
    if not value.endswith('@example.com'):
        raise ValidationError(
            _('Invalid email address. Only example.com addresses are allowed.')
        )


class PasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

        if not re.findall('[A-Z]', password):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.findall('[a-z]', password):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.findall('[0-9]', password):
            raise ValidationError(
                "Password must contain at least one number"
            )

        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(
                "Password must contain at least one special character"
            )

    def get_help_text(self):
        return _(
            'Your password must contain at least 8 characters, including one uppercase letter, '
            'one lowercase letter, one digit, and one special character.'
        )
