from celery import shared_task
from .models import Comment
from .notifications import notify_consumers


@shared_task
def handle_comment_created_event(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        notify_consumers(comment, method='comment_created', group='comments')
    except Exception as e:
        pass
