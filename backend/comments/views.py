from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ViewSet):

    queryset = Comment.objects.all().order_by('-created_at')
    serializer = CommentSerializer

    def list(self, request):
        serializer = self.serializer(self.queryset.filter(parent=None), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs.get('pk', None))
        serializer = self.serializer(instance)
        return Response(serializer.data)
