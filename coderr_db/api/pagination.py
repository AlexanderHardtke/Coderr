from rest_framework.pagination import PageNumberPagination


class   SmallResultSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 99
    page_query_param = 'page'