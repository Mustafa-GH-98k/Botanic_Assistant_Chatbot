from functools import wraps
from flask import request, jsonify

from Models.api_response import ApiResponse

from flask import request
from Config.constants import API_VERSION 

def authenticate_api_key(api_header, valid_apikeys_getter):
    """Decorator to authenticate API key from request headers.

    Args:
        api_header (str): The name of the header to check for the API key.
        valid_apikeys_getter (Callable): A function to retrieve valid API keys.

    Returns:
        Callable: Decorator function that wraps the original function.

    Example:
        @authenticate_api_key('x-api-key', lambda: ['valid_key1', 'valid_key2'])
        def my_function():
            pass
    """
    def decorator(f):
        """Inner decorator function.

        Args:
            f (Callable): The function to wrap.

        Returns:
            Callable: The wrapped function.
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            """Wrapper function to check the API key.

            Args:
                *args: Positional arguments for the wrapped function.
                **kwargs: Keyword arguments for the wrapped function.

            Returns:
                Response: JSON response if authentication fails, otherwise calls the original function.

            Raises:
                Exception: If there is an unexpected error processing the request.

            Example:
                @authenticate_api_key('x-api-key', lambda: ['valid_key'])
                def my_protected_function():
                    return "Protected content"
            """
            header_value = request.headers.get(api_header)
            
            if header_value is None:
                return ApiResponse(
                    status_code=401,
                    success=False,
                    error_messages=[f"'{api_header}' header is required"]
                ).to_json()

            if header_value not in valid_apikeys_getter():
                return ApiResponse(
                    status_code=403,
                    success=False,
                    error_messages=[f"Invalid value for '{api_header}'"]
                ).to_json()

            return f(*args, **kwargs)  
        return wrapper
    return decorator
