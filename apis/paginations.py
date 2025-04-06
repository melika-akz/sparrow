from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'take'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        paginator = self.django_paginator_class(queryset, self.page_size)
        page_number = request.query_params.get(self.page_query_param, 1)

        try:
            self.page = paginator.page(page_number)
        except EmptyPage:
            self.page = []
            self.request = request
            self.paginator = paginator
            return []

        self.request = request
        self.paginator = paginator
        return list(self.page)

    def get_paginated_response(self, data):
        if isinstance(self.page, list):
            return Response({
                'count': self.paginator.count,
                'next': None,
                'previous': None,
                'results': []
            })

        return super().get_paginated_response(data)

