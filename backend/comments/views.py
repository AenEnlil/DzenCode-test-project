from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Exists, OuterRef
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Comment
from .serializers import CommentSerializer, CommentDetailsSerializer
from .paginators import CommentsListPaginator, RepliesPaginator


class CommentViewSet(GenericViewSet, ListModelMixin):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['email', 'username', 'created_at']
    ordering = ['-created_at']
    pagination_classes = {'list': CommentsListPaginator, 'get_replies': RepliesPaginator}

    def get_pagination_class(self):
        return self.pagination_classes.get(self.action, None)

    def paginate_queryset(self, queryset):
        pagination_class = self.get_pagination_class()
        if pagination_class is None:
            return None

        paginator = pagination_class()
        self._dynamic_paginator = paginator
        return paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        paginator = getattr(self, '_dynamic_paginator', None)
        if paginator is None:
            return Response(data)
        return paginator.get_paginated_response(data)

    def get_serializer_class(self):
        if self.action == 'get_replies' or self.action == 'retrieve':
            return CommentDetailsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(parent=None)
        elif self.action == 'get_replies':
            queryset = queryset.filter(parent_id=self.kwargs.get('pk'))
        return queryset

    def notify_consumers(self, method: str, group: str, data: str):
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group,
                {
                    "type": method,
                    "data": data
                }
            )
        except Exception as e:
            pass

    @method_decorator(cache_page(5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, kwargs)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        self.notify_consumers(method='comment_created', group='comments', data=data)
        return Response(data)

    @method_decorator(cache_page(10))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.has_replies = Comment.objects.filter(parent=instance.id).exists()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @method_decorator(cache_page(5))
    @action(methods=['get'], detail=False, url_path='(?P<pk>[0-9]+)/replies')
    def get_replies(self, request, *args, **kwargs):
        # check if replies has nested replies
        subquery = Comment.objects.filter(parent=OuterRef('pk'))
        queryset = self.get_queryset().order_by('-created_at').annotate(has_replies=Exists(subquery))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
