from functools import wraps
from flask import request, jsonify

from Models.api_response import ApiResponse

from flask import request
from Config.constants import API_VERSION 

def validate_headers(required_headers, allowed_values):
    """Decorator to validate request headers.

    Args:
        required_headers (list): A list of headers that must be present in the request.
        allowed_values (dict): A dictionary mapping header names to a list of allowed values.

    Returns:
        Callable: Decorator function that wraps the original function.

    Example:
        @validate_headers(['Content-Type'], {'Content-Type': ['application/json']})
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
            """Wrapper function to validate headers.

            Args:
                *args: Positional arguments for the wrapped function.
                **kwargs: Keyword arguments for the wrapped function.

            Returns:
                Response: JSON response if validation fails, otherwise calls the original function.

            Example:
                @validate_headers(['Authorization'], {'Authorization': ['Bearer token']})
                def my_protected_function():
                    return "Protected content"
            """
            for required_header in required_headers:
                header_value = request.headers.get(required_header)
                
                if header_value is None:
                    return ApiResponse(
                        status_code=400,
                        success=False,
                        error_messages=[f"'{required_header}' header is required"]
                    ).to_json()

                if header_value not in allowed_values.get(required_header, []):
                    return ApiResponse(
                        status_code=400,
                        success=False,
                        error_messages=[f"Invalid value for '{required_header}'. Allowed values are: {', '.join(allowed_values.get(required_header, []))}"]
                    ).to_json()

            return f(*args, **kwargs)  
        return wrapper
    return decorator
