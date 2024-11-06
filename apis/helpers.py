from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(exc, ValidationError) and response.status_code not in [200, 201]:
            if isinstance(response.data, list):
                detail = response.data[0]
            else:
                detail = response.data.get('non_field_errors', ['Validation error occurred.'])[0]

            response.data = {
                'status_code': response.status_code,
                'detail': detail
            }

    return response

