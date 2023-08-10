"""
Exception class for wrapping errors that can occur when interfacing with the NYPL backend.
"""
class NyplBackendException(Exception):

    def __init__(self, msg, e=None):
        super(NyplBackendException, self).__init__(msg, e)
        self.message = msg
