# coding=utf-8
"""
This class contains all stuff regarding recipient handling.
"""
from abc import ABCMeta


class RecipientsListEntry(metaclass=ABCMeta):
    """
    This is an abstract class defining an entry for the compound class RecipientsList.
    """
    pass


class RecipientsList(RecipientsListEntry):
    """
    This class is basically a list wrapper with specialized functions regarding the handling of its entries.
    """
    pass


class Recipient(RecipientsListEntry):
    """
    This class models an email recipient contained in a RecipientsList.
    """
    pass
