from django.db import models


class Comment(models.Model):
    text = models.TextField()
    username = models.CharField()
    email = models.EmailField()
    homepage = models.URLField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
