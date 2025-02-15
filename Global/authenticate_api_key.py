from functools import wraps
from flask import request, jsonify

from Global.Models.api_response import ApiResponse

from flask import request
from Global.static import API_VERSION 

def authenticate_api_key(api_header, valid_apikeys_getter):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

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
