import re

from rest_framework import serializers
from .models import Comment
from .validators import HtmlTagValidator


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_text(self, value):
        regex = re.compile(r'<[a-zA-Z\/][^>]*>')
        if regex.search(value):
            HtmlTagValidator().validate(value)

        return value


class CommentDetailsSerializer(CommentSerializer):
    has_replies = serializers.BooleanField()
