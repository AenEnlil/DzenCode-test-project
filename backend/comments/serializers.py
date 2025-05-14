import re

from django.conf import settings
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


class CommentFilesUrlSerializer(CommentSerializer):
    image = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'image', 'file', 'username', 'email', 'homepage', 'parent', 'created_at')

    def get_image(self, obj):
        if obj.image:
            return f'{settings.BASE_URL}{obj.image.url}'
        return None

    def get_file(self, obj):
        if obj.file:
            return f'{settings.BASE_URL}{obj.file.url}'
        return None


class CommentDetailsSerializer(CommentFilesUrlSerializer):
    has_replies = serializers.BooleanField()

    class Meta:
        model = Comment
        fields = '__all__'
