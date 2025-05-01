import re

from django.core.validators import RegexValidator

alphanumeric_validator = RegexValidator(regex=r'^[a-zA-Z0-9]+$')
