# -*- coding: utf-8 -*-
"""
Flow related exceptions
"""

class FlowException(Exception):
    """Base class for exceptions in flow."""
    pass

class FlowConfigFileNotFoundException(FlowException):
    """Exception raised for errors in the task validations.

    Attributes:
        filePath -- missing config file
    """

    def __init__(self, filePath: str):
        self.message = filePath

class FlowConfigException(FlowException):
    """Exception raised for errors in the task validations.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str):
        self.message = message
