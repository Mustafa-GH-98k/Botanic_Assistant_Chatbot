class ServiceException(Exception):
    """Base class for service exceptions."""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code

