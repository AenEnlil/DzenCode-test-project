from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .tasks import handle_comment_created_event


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        handle_comment_created_event.delay(instance.id)
