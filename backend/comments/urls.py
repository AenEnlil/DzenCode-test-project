from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet

comments_router = SimpleRouter()
comments_router.register('', CommentViewSet)

urlpatterns = [
    path('', include(comments_router.urls))
]
