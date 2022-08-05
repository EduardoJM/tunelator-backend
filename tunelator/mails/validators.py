import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class UserMailAliasValidator(validators.RegexValidator):
    regex = r'^[\w\d_]+$'
    message = _(
        'Use an valid e-mail username.'
    )
    flags = 0
