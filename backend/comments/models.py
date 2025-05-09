from django.core.validators import MinLengthValidator
from django.db import models

from .validators import alphanumeric_validator


class Comment(models.Model):
    text = models.TextField(max_length=1500)
    username = models.CharField(max_length=60, validators=[MinLengthValidator(3), alphanumeric_validator])
    email = models.EmailField()
    homepage = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to='files', null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
