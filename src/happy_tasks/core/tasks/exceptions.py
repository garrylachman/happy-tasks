# -*- coding: utf-8 -*-
"""
Task related exceptions
"""

class TaskException(Exception):
    """Base class for exceptions in task."""
    pass

class TaskValidationException(TaskException):
    """Exception raised for errors in the task validations.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str):
        self.message = message
