from flask import jsonify

from Config.constants import API_VERSION

class ApiResponse:
    """
    This class represents a standardized API response that is returned by the API.
    
    Example :
        response = ApiResponse(200, True, "Hello, world!")
        return response.to_json()
    """
    def __init__(self, status_code: int, success: bool, response=None, error_messages=None, version=API_VERSION):
        self.status_code = status_code
        self.success = success
        self.response = response
        self.error_messages = error_messages
        self.version = version

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "success": self.success,
            "response": self.response,
            "error_messages": self.error_messages,
            "version": self.version
        }

    def to_json(self):
        return jsonify(self.to_dict()), self.status_code

