from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(GenericViewSet, ListModelMixin):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['email', 'username', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(parent=None)
        elif self.action == 'get_replies':
            queryset = queryset.filter(parent_id=self.kwargs.get('pk'))
        return queryset

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='(?P<pk>[0-9]+)/replies')
    def get_replies(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-created_at')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
