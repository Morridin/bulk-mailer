# coding=utf-8
"""
This class contains all stuff regarding recipient handling.
"""
class Recipient:
    """
    This class models an email recipient contained in a RecipientsList.
    Important note: The __str__ method only returns the first e-mail entered for each recipient!
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

    def __str__(self) -> str:
        return f"{self.name} <{self.addresses[0]}>"


class RecipientsList:
    """
    This class is basically a list wrapper with specialized functions regarding the handling of its entries.
    """
    def __init__(self):
        self.recipients: list[Recipient] = []

    def __len__(self) -> int:
        return len(self.recipients)


    def __getitem__(self, item: int) -> Recipient:
        return self.recipients[item]

    def append(self, item: Recipient) -> None:
        """
        This method adds a new element to the end of the list.
        :param item: The new list item.
        :return: None
        """
        self.recipients.append(item)

