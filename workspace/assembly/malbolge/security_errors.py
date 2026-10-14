"""security_errors.py - categorias de error del vocabulario."""

from enum import Enum


class ErrorCategory(Enum):
    UNKNOWN = 0
    PERMISSION = 1
    BOUNDARY = 2
    INTEGRITY = 3
    AUTHORITY = 4
    VALIDATION = 5
    RESOURCE = 6
    INTERNAL = 7


ERROR_CATEGORY_NAMES = [c.name for c in ErrorCategory]
