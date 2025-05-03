from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError
from rest_framework.test import APITestCase
from ..validators import alphanumeric_validator, HtmlTagValidator


class AlphanumericValidatorTests(APITestCase):

    def test_valid_text_not_raise_error(self):
        data = 'tesT123'
        alphanumeric_validator(data)

    def test_text_with_only_digits_not_raise_error(self):
        data = '123'
        alphanumeric_validator(data)

    def test_text_with_only_letters_not_raise_error(self):
        data = 'Test'
        alphanumeric_validator(data)

    def test_text_with_special_symbols_raise_error(self):
        data = 't#est123'
        with self.assertRaises(ValidationError):
            alphanumeric_validator(data)

    def test_text_with_cyrillic_letters_raise_error(self):
        data = 'тест123'
        with self.assertRaises(ValidationError):
            alphanumeric_validator(data)


class HtmlTagValidatorTest(APITestCase):

    def setUp(self):
        self.validator = HtmlTagValidator()
        self.whitelist_tags = settings.ALLOWED_HTML_TAGS
        self.whitelist_attributes = settings.ALLOWED_HTML_ATTRIBUTES

    def test_text_without_tags_not_raise_error(self):
        data = 'text'
        self.validator.validate(data)

    def test_text_with_allowed_tags_not_raise_error(self):
        for tag in self.whitelist_tags:
            data = f'<{tag}>text</{tag}>'
            self.validator.validate(data)

    def test_text_with_allowed_attributes_not_raise_error(self):
        for tag in self.whitelist_attributes:
            for attribute in self.whitelist_attributes.get(tag, []):
                data = f'<{tag} {attribute}=\"asd\">text</{tag}>'
                self.validator.validate(data)

    def test_text_with_forbidden_tag_raise_error(self):
        data = '<img>text</img>'
        with self.assertRaises(DrfValidationError):
            self.validator.validate(data)

    def test_text_with_not_allowed_attribute_raise_error(self):
        tag = self.whitelist_tags[0]
        data = f'<{tag} style=\"asd\">text</{tag}>'
        with self.assertRaises(DrfValidationError):
            self.validator.validate(data)

    def test_text_with_unclosed_tag_raise_error(self):
        tag = self.whitelist_tags[0]
        data = f'<{tag}>text'
        with self.assertRaises(DrfValidationError):
            self.validator.validate(data)
