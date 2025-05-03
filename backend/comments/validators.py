from bs4 import BeautifulSoup
from django.core.validators import RegexValidator
from django.conf import settings
from rest_framework.exceptions import ValidationError

alphanumeric_validator = RegexValidator(regex=r'^[a-zA-Z0-9]+$')


class HtmlTagValidator:
    allowed_tags = settings.ALLOWED_HTML_TAGS
    allowed_attributes = settings.ALLOWED_HTML_ATTRIBUTES
    escaped_symbols = {'&lt;': '<', '&gt;': '>', '&amp;': '&'}

    def replace_escaped_symbols(self, string: str) -> str:
        """
        Replaces html related characters that Soup escaped
        :param string: string with escaped chars
        :return: modified string without escaped chars
        """
        for symbol in self.escaped_symbols:
            string = string.replace(symbol, self.escaped_symbols.get(symbol))
        return string

    def validate(self, value: str) -> None:
        soup = BeautifulSoup(value, "html.parser")

        for tag in soup.find_all(True):
            if tag.name not in self.allowed_tags:
                raise ValidationError(f"Tag <{tag.name}> is forbidden")

            allowed_attrs = self.allowed_attributes.get(tag.name, [])
            for attr in tag.attrs:
                if attr not in allowed_attrs:
                    raise ValidationError(f"Attribute '{attr}' is forbidden in <{tag.name}>.")

        cleaned_text = self.replace_escaped_symbols(str(soup))
        # soup automatically closes tags, so we check if soup text is different from original
        if cleaned_text != value:
            raise ValidationError("Text contains unclosed html tags or syntax error")
