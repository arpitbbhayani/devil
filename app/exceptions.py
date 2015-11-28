class DevilException(Exception):
    status_code = 500
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class UnsupportedException(DevilException):
    def __init__(self, message, status_code=None, payload=None):
        DevilException.__init__(self, message, status_code, payload)

class AuthorizationException(DevilException):
    def __init__(self, message, status_code=None, payload=None):
        DevilException.__init__(self, message, status_code, payload)

class ResourceExhaustException(DevilException):
    def __init__(self, message, status_code=None, payload=None):
        DevilException.__init__(self, message, status_code, payload)
