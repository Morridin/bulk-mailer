# coding=utf-8
"""
This file provides the interface between the user interface and the program routines behind.
"""
from typing import Any

from lib import UI
from lib.recipients import RecipientsList, Recipient, RecipientManagement
from lib.server_connections import ServerConnectionList, ServerConnection, ServerConnectionManagement

SCM: ServerConnectionManagement = ServerConnectionManagement()
RM: RecipientManagement = RecipientManagement()


def init(interface: UI) -> None:
    """
    This method is called on program start and runs the user interface.
    :param interface: the interface to start
    :return: None
    """
    interface.init()


def server_connections_get_list() -> ServerConnectionList:
    """
    This function provides the calling user interface with the ServerConnectionList the program holds.
    :return: A ServerConnectionList object
    """
    raise NotImplementedError()


def server_connections_add_new(new_entry: ServerConnection, active: bool) -> None:
    """
    This function provides a direct way to add a new entry to the ServerConnectionList object the program holds without
    the need for the UI to get the list in before.
    :param new_entry: The ServerConnection object that is to be added.
    :param active: Tells the program to set this ServerConnection as the active one.
    :return: None
    """
    SCM.add_new_entry(new_entry, active)


def recipients_get_list() -> RecipientsList:
    """
    Works the same way as server_connections_get_list.
    :return: See for yourself.
    """
    raise NotImplementedError()


def recipients_add_new(new_entry: Recipient) -> None:
    """
    This function adds a new entry into the main recipients list
    :param new_entry: The Recipient to be added
    :return: None
    """
    _ = (new_entry,)
    raise NotImplementedError()


def recipients_clear() -> None:
    """
    Asks the program to erase all recipients from the list.
    :return: None
    """
    raise NotImplementedError()


def message_load_file(path: str) -> bool:
    """
    Asks the program to load an email message from the file specified in path.
    :param path: The path to the file containing the email message.
    :return: True, if the file could be opened and the email could be loaded.
    """
    _ = (path,)
    return False


def message_clear() -> None:
    """
    See recipients_clear().
    :return: None
    """
    raise NotImplementedError()


def get_status() -> dict:
    """
    Asks the program to let out some stats about its current status.
    :return: a dict containing such information.
    """
    raise NotImplementedError()


def send_message(output_stream: Any) -> Any:
    """
    This function tells the program to send the message to all recipients in the list using the currently active server
    connection. Also, it gives info to the user interface (via the output_stream param) about what's going on.
    :param output_stream: A stream object in which the info from the sending can be piped...
    :return: Don't know yet.
    """
    _ = (output_stream,)
    raise NotImplementedError()


def total_reset() -> None:
    """
    This function tells the program to forget about everything and to reset on initial values.
    :return: None
    """
    raise NotImplementedError()


def die() -> None:
    """
    This function offers a "safe" exit out of the program.
    :return: None
    """
    exit(0)
