from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MemberPagination(PageNumberPagination):
    """
    Custom pagination for Member list view.
    """
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to override page size
    max_page_size = 100  # Maximum page size allowed
    page_query_param = 'page'  # Page number parameter

    def get_paginated_response(self, data):
        """
        Return a paginated response with custom format.
        """
        return Response({
            'count': self.page.paginator.count,  # Total number of items
            'total_pages': self.page.paginator.num_pages,  # Total number of pages
            'current_page': self.page.number,  # Current page number
            'next': self.get_next_link(),  # URL for next page
            'previous': self.get_previous_link(),  # URL for previous page
            'results': data  # The actual data
        })
