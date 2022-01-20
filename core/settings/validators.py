from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


class DigitOrSymbolPasswordValidator:
    symbols = """[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]"""
    digits = "[0-9]"

    def validate(self, password, user=None):
        if not (re.findall(self.symbols, password) or re.findall(self.digits, password)):
            raise ValidationError(
                """The password must contain at least either 1 digit or 1 symbol.""",
                code='password_no_digit_or_symbol'
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit or 1 symbol."
        )


class UppercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter."
        )


class LowercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter."
        )
