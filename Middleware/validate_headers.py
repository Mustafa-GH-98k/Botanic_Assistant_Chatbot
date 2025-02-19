from functools import wraps
from flask import request, jsonify

from Models.api_response import ApiResponse

from flask import request
from Config.constants import API_VERSION 

def validate_headers(required_headers, allowed_values):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
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
