from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CommentsListPaginator(PageNumberPagination):
    page_size = 25


class RepliesPaginator(LimitOffsetPagination):
    default_limit = 10
