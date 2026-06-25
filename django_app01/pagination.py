from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    ordering = '-created_at'
    page_size = 6
    page_size_query_param = 'page_size'


