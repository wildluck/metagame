"""
Metagames Project License

Copyright (c) 2024 Rishat Maksudov

Permission is granted to use, modify, and distribute this software for any purpose, with proper credit to the original author.

This software is provided "as is," without any warranty of any kind. The author is not responsible for any damages arising from its use.

"""


from enum import Enum, unique

@unique
class RequestType(Enum):
    """
    Enumeration for different types of client requests.

    Attributes:
        LOG_IN: Request to log in.
        LOG_OUT: Request to log out.
        GET_BALANCE: Request to get account balance.
        BUY_ITEM: Request to buy an item.
        SELL_ITEM: Request to sell an item.
    """
    LOG_IN = 1
    LOG_OUT = 2
    GET_BALANCE = 3
    BUY_ITEM = 4
    SELL_ITEM = 5