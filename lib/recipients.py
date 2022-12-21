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
    def __init__(self, name: str, *email: str):
        self.name: str = name
        self.addresses: list[str] = list(email)

    def add_address(self, address: str) -> None:
        """
        This method adds an address to the recipient.
        :param address: The address to be added.
        :return: None
        """
        self.addresses.append(address)

    def get_formatted(self) -> tuple[str]:
        """
        This method creates a tuple of strings that read like 'Recipient <address@example.com>'.
        :return: See above.
        """
        out: list[str] = []
        for address in self.addresses:
            out.append(f"{self.name} <{address}>")
        return tuple(out)
