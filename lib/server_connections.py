# coding=utf-8
"""
This file contains the functionality regarding the connection to the smtp/imap servers.

IMAP is required in order to catch error messages that arise from sending emails to addresses not existing. Or to people
with a full mailbox.

As I regard using IMAP rather as a convenience feature than a required feature, IMAP will be added later.
"""
from enum import Enum

from lib.recipients import Recipient


class Encryption(Enum):
    """
    This enum holds all available options for connection encryption.
    """
    SSL = 1
    STARTTLS = 2


class ServerConnection:
    """
    This class represents a complete smtp/imap server config.
    """

    def __init__(self,
                 name: str,
                 smtp_host: str,
                 smtp_port: int,
                 sender_name: str,
                 sender_email: str,
                 smtp_encryption: bool | Encryption = False,
                 smtp_login: bool = False,
                 imap_host: str = None,
                 imap_port: int = None,
                 imap_encryption: bool | Encryption = False,
                 imap_login: bool = False,
                 share_login: bool = True,
                 smtp_credentials: tuple[str, str] = None,
                 imap_credentials: tuple[str, str] = None):
        if smtp_credentials is not None or imap_credentials is not None:
            raise NotImplementedError("No auth credential storage implemented yet!")
        self.smtp = {
            "host": smtp_host,
            "port": smtp_port,
            "encryption": smtp_encryption,
            "login": smtp_login,
            "credentials": None
        }
        self.imap = {
            "host": imap_host,
            "port": imap_port,
            "encryption": imap_encryption,
            "login": imap_login,
            "credentials": None
        }
        self.share_login = share_login
        self.sender = Recipient(sender_name, sender_email)
        self.name = name


class ServerConnectionList:
    """
    This class holds the list of all ServerConnection objects in the application.
    """

    def __init__(self):
        self.connections: list[ServerConnection] = []
        self.active: int = -1

    def __len__(self):
        return len(self.connections)

    def delete(self, i):
        """
        Removes the element with index i from the ConnectionList. This is opposite to the not implemented method remove,
        which goes for the element to remove as the parameter.
        :param i: The index of the element in the ConnectionList to be removed. Must be in range  [0, len(list))
        """
        if 0 <= i < len(self):
            if i == self.active:
                self.active = -1
            if i < self.active:
                self.active -= 1
            return self.connections.pop(i)
        else:
            raise IndexError("List index out of range.")

    def set_active(self, i: int) -> bool:
        """
        Sets the list item with index i as the active ServerConnection.
        :param i: The list index of the ServerConnection that is meant to set as active one.
                  Must be in range  [0, len(list))
        :return: True, if the operation was successful. False otherwise, which is, if i is not a valid index.
        """
        if 0 <= i < len(self):
            self.active = i
            return True
        else:
            return False

    def __getitem__(self, item: int) -> ServerConnection:
        return self.connections[item]

    def append(self, new_item: ServerConnection, as_active: bool = False) -> None:
        """
        This method adds a new item to the list.
        :param new_item: the new item to add
        :param as_active: a flag that states, if the new item shall be set as the active one.
        :return: None.
        """
        if as_active:
            self.active = len(self.connections)
        self.connections.append(new_item)
