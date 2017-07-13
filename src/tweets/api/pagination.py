#it's about how many item size in a page


from rest_framework import pagination

class StandardResultsPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000