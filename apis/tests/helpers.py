import json
from rest_framework.test import APITransactionTestCase


def _client(
        test_case: APITransactionTestCase,
        method: str,
        path: str,
        data: dict = None
):
    """Custom client function to handle API requests.

    Args:
        test_case (APITransactionTestCase): An instance of APITransactionTestCase for making requests.
        method (str): The HTTP method (e.g., 'POST', 'PUT', 'PATCH', 'DELETE').
        path (str): The API endpoint to request.
        data (dict, optional): The data to send with the request. Defaults to None.

    Returns:
        Response: The response from the API.
    """
    if data is not None:
        data = json.dumps(data)

    response = test_case.client.generic(
        method,
        path,
        data=data,
        content_type='application/json'
    )
    return response

