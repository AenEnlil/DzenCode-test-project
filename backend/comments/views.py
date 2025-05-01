from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(GenericViewSet):

    queryset = Comment.objects.all().order_by('-created_at')
    serializer = CommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(parent=None)
        elif self.action == 'get_replies':
            queryset = queryset.filter(parent_id=self.kwargs.get('pk'))
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='(?P<pk>[0-9]+)/replies')
    def get_replies(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer(queryset, many=True)
        return Response(serializer.data)
