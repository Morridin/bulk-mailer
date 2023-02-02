# coding=utf-8
"""
This file provides the interface between the user interface and the program routines behind.
"""
import copy
import io
import smtplib
from collections import defaultdict
from email.message import EmailMessage
from email.parser import BytesParser, Parser
from email.policy import EmailPolicy
from enum import Enum
from typing import Any

from lib.recipients import RecipientsList, Recipient
from lib.server_connections import ServerConnectionList, ServerConnection, Encryption
from lib.ui import UI

_SCL: ServerConnectionList = ServerConnectionList()
_RL: RecipientsList = RecipientsList()
_MSG: EmailMessage = EmailMessage()


class SendStatus(Enum):
    """
    This enum contains a collection of various possible endings for the send mail function.
    """
    OK = (0, "All recipients received their email.")
    SMTP_GENERIC_ERROR = (100, "The SMTP server sent an unexpected status code.")
    SMTP_MISSING_LOGIN_DATA = (101, "The SMTP server required login data, that was not delivered.")
    SMTP_HELO = (102, "The SMTP server didn't reply properly on HELO greeting when sending an email.")
    SMTP_SENDER_REFUSED = (103, "The SMTP server didn't accept the sender email as valid.")
    SMTP_RECIPIENT_REFUSED = (104, "At least one recipient was invalid or did not receive its email.")


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
    return _SCL


def server_connections_add_new(new_entry: ServerConnection, active: bool) -> None:
    """
    This function provides a direct way to add a new entry to the ServerConnectionList object the program holds without
    the need for the ui to get the list in before.
    :param new_entry: The ServerConnection object that is to be added.
    :param active: Tells the program to set this ServerConnection as the active one.
    :return: None
    """
    _SCL.append(new_entry, active)


def recipients_get_list() -> RecipientsList:
    """
    Works the same way as server_connections_get_list.
    :return: See for yourself.
    """
    return _RL


def recipients_add_new(new_entry: Recipient) -> None:
    """
    This function adds a new entry into the main recipients list
    :param new_entry: The Recipient to be added
    :return: None
    """
    _RL.append(new_entry)


def recipients_clear() -> None:
    """
    Asks the program to erase all recipients from the list.
    :return: None
    """
    global _RL
    _RL = RecipientsList()


def message_load_file(path: str) -> bool:
    """
    Asks the program to load an email message from the file specified in path.
    :param path: The path to the file containing the email message.
    :return: True, if the file could be opened and the email could be loaded.
    """
    try:
        with open(path, encoding="utf8") as fp:
            global _MSG
            parser = BytesParser(policy=EmailPolicy().clone(utf8=True))
            if isinstance(fp, io.TextIOBase):
                parser = Parser(policy=EmailPolicy().clone(utf8=True))
            _MSG = parser.parse(fp)
            _MSG.set_charset("utf-8")
            del _MSG["From"]
            del _MSG["To"]
            return True
    except OSError:
        return False


def message_clear() -> None:
    """
    See recipients_clear().
    :return: None
    """
    global _MSG
    _MSG = EmailMessage()


def get_status() -> dict:
    """
    Asks the program to let out some stats about its current status.
    :return: a dict containing such information.
    """
    raise NotImplementedError()


def send_message(output_stream: io.TextIOBase, *, smtp_user: str = None, smtp_password: str = None, imap_user: str = None,
                 imap_password: str = None) -> tuple[SendStatus, str]:
    """
    This function tells the program to send the message to all recipients in the list using the currently active server
    connection. Also, it gives info to the user interface (via the output_stream param) about what's going on.
    :param output_stream: A stream object in which the info from the sending can be piped...
    :param smtp_user: If the SMTP server requires authentication, use this parameter to transmit the smtp username
    :param smtp_password: If the SMTP server requires authentication, place the smtp password here.
    :param imap_user: Same as with smtp_user, just for IMAP server. *Currently not used!*
    :param imap_password: Same as with smtp_user, just for IMAP server. *Currently not used!*
    :return: Don't know yet.
    """
    # TODO: Catch ssl.SSLError upon using encrypted connections!
    _ = (imap_user, imap_password)

    connection: ServerConnection = _SCL.get_active()
    with connection.get_smtp() as smtp:
        if connection.smtp["encryption"] == Encryption.STARTTLS:
            smtp.starttls()
        if connection.smtp["login"]:
            if smtp_user is None or smtp_password is None:
                return SendStatus.SMTP_MISSING_LOGIN_DATA, ""
            try:
                smtp.login(smtp_user, smtp_password)
            except smtplib.SMTPAuthenticationError as login_fail:
                return SendStatus.SMTP_GENERIC_ERROR, login_fail.smtp_error
            except smtplib.SMTPHeloError:
                return SendStatus.SMTP_HELO, ""
            except (smtplib.SMTPNotSupportedError, smtplib.SMTPException) as ex:
                return SendStatus.SMTP_GENERIC_ERROR, str(ex)
        else:
            smtp.ehlo_or_helo_if_needed()

        # Send messages, handle errors occuring.
        refused: dict[str, tuple[int, bytes]] = defaultdict(tuple[int, bytes])
        for i, recipient in enumerate(_RL):
            print(f"Sending email {i} of {len(_RL)}...", file=output_stream, flush=True)
            rcpt_copy: EmailMessage = copy.deepcopy(_MSG)
            rcpt_copy.add_header("From", str(connection.sender))
            rcpt_copy.add_header("To", ", ".join(recipient.get_formatted()))
            try:
                refused |= smtp.send_message(rcpt_copy)
                print(f"\tSent!", file=output_stream, flush=True)
            except smtplib.SMTPRecipientsRefused as total_fail:
                refused |= total_fail.recipients
                print(f"\tSent!", file=output_stream, flush=True)
            except smtplib.SMTPHeloError:
                return SendStatus.SMTP_HELO, ""
            except smtplib.SMTPSenderRefused:
                return SendStatus.SMTP_SENDER_REFUSED, str(connection.sender)
            except smtplib.SMTPDataError as generic:
                return SendStatus.SMTP_GENERIC_ERROR, f"{generic.smtp_code}: {generic.smtp_error}"
            except smtplib.SMTPNotSupportedError:
                return SendStatus.SMTP_GENERIC_ERROR, "You did something evil."

        # If we came until here, the sending has somewhat worked, but we might have some recipients who didn't make it.
        if len(refused) == 0:
            return SendStatus.OK, ""
        else:
            return SendStatus.SMTP_RECIPIENT_REFUSED, str(refused)


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
