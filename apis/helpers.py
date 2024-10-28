from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

        if isinstance(exc, ValidationError):
            response.data = {
                'status_code': response.status_code,
                'detail': response.data.get('non_field_errors', ['Validation error occurred.'])[0]
            }

    return response

