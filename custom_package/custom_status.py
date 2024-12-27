"""
Metagames Project License

Copyright (c) 2024 Rishat Maksudov

Permission is granted to use, modify, and distribute this software for any purpose, with proper credit to the original author.

This software is provided "as is," without any warranty of any kind. The author is not responsible for any damages arising from its use.

"""


from enum import Enum, unique

@unique
class ResponseStatus(Enum):
    """
    Enumeration for server response statuses.

    Attributes:
        SUCCESS: Indicates the operation was successful.
        ERROR: Indicates the operation failed.
    """
    SUCCESS = 200
    ERROR = 300