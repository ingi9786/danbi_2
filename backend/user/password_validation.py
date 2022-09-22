import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumericSpecialCharValidator:
    """
    숫자, 특수문자를 포함하도록 검사하는 validator
    """
    @classmethod
    def validate(cls, password, user=None):
        regex = re.compile(r'(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\W\s_]).*')
        if re.search(regex, password) is None:
            raise ValidationError(
                _("Try another password!"),
                code="password_validate_error",
            )
        return True

    def get_help_text(self):
        return _("Password contain at least 'one special character' and 'one numeric character'!")
