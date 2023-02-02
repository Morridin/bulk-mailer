# coding=utf-8
"""
This file holds all the stuff needed for a command line ui for the bulk mailer program.
"""
import argparse
import platform
import subprocess
import sys
import time
from getpass import getpass
from typing import Any, Callable, Union, Optional, Sequence

import lib
from lib import engine
from lib.recipients import Recipient
from lib.server_connections import Encryption, ServerConnection, ServerConnectionList
from lib.ui import UI


class CommandLine(UI):
    """
    This class bundles the interactive command line user interface.
    """
    headline = f"Bulk Mailer v{lib.__version__}"

    def __init__(self):
        self.command_stack: list[Callable] = []  # A stack containing the last menus called
        self.next_command: Optional[Callable] = None

    def init(self) -> None:
        """
        Starts the interactive command line application.
        """
        while True:
            # Chose the correct command to be the next current one.
            if self.next_command is None:
                if len(self.command_stack) == 0:
                    current_command = main_menu
                else:
                    current_command = self.command_stack.pop()
            else:
                current_command = self.next_command

            # Execute that command and thus gather the next one.
            self.next_command = current_command()

            # In case we don't want to go back in the menu hierarchy, save the last command for later.
            if self.next_command is not None:
                self.command_stack.append(current_command)


def _clear_screen():
    """
    This function clears the console screen.
    """
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear_screen"])
    print(CommandLine.headline)


def _create_input_message(item: str) -> str:
    """
    This function adds the value in item into a standard "Please enter X" input prompt and returns the input result.
    :param item: A textual description of what is expected.
    :return: The input of the user.
    """
    return input(f"Please enter {item}: ")


def _print_menu(menu_name: str,
                menu_options: Sequence[str],
                menu_actions: Sequence[Optional[Callable[[], Union[Callable, None]]]], *,
                special_text: str = None,
                input_text: str = None) -> Optional[Callable[[], Union[Callable, None]]]:
    """
    This function prints a menu and returns the choice of the user.
    :param menu_name: The name of the menu to print
    :param menu_options: The options in the menu to print
    :param menu_actions: The list of actions that correspond to
    the options in the menu.
    :param special_text: If the screen to show is no menu (or the "You are in menu X" text
    doesn't fit), use this parameter to hand in your own text.
    :param input_text: If you want to enter a different input message, use this keyword-argument.
    :return: The chosen action
    """
    if input_text is None:
        input_text = "the number of the action you want to perform"
    _clear_screen()
    if special_text is None:
        print(f"You are currently in the {menu_name}.\nYou have the following options:\n")
    else:
        print(special_text)

    actions: dict[str, Optional[Callable[[], Union[Callable, None]]]] = {}
    counter_width: int = len(str(len(menu_options)))

    for i, (option, action) in enumerate(zip(menu_options, menu_actions), 1):
        print(f"{i:>{counter_width}}. {option}")
        actions[f"{i}"] = action

    print("")
    choice = _create_input_message(input_text)
    while choice not in actions:
        print("This is not a valid option!")
        choice = _create_input_message(input_text)

    return actions[choice]


def _is_int(s: str) -> int:
    """
    This function is a dirty approach to test, if a string can be converted into an int.
    :param s: the str object to be tested for transferability to int.
    :return: True, if s can be converted to int, False otherwise.
    """
    try:
        _ = int(s)
    except ValueError:
        return False
    return True


def _get_pseudo_bool_option(question_text: str, options: Sequence[tuple[str, Any]]) -> Any:
    """
    This function asks the user a question and presents a set of answer options.
    It returns the value of the selected option.
    Attention: This function does not clear the screen!
    :param question_text: The text of the question to ask the user.
    :param options: A list consisting of tuples consisting of the displayed answers and their associated values.
    :return: the value of the selected option.
    """
    input_text: str = "the number of the best fitting option"
    print(f"{question_text}\n")

    counter_width: int = len(str(len(options)))
    values: dict[str, Any] = {}

    for i, (option, value) in enumerate(options, 1):
        print(f"{i:>{counter_width}}. {option}")
        values[f"{i}"] = value

    print("")
    choice = _create_input_message(input_text)
    while choice not in values:
        print("This is not a valid option!")
        choice = _create_input_message(input_text)

    return values[choice]


def main_menu() -> Union[Callable[[], None], None]:
    """
    This function shows the main menu.
    :return: A callable representing the action chosen in the main menu.
    """
    name = "main menu"
    options = [
        "Manage Connections to mail servers",
        "Manage recipients list",
        "Manage email message",
        "Get current application status",
        "Send an email using the message, setup and recipients according to the current application status",
        "Reset the application",
        "Exit"
    ]
    actions = [
        server_manage,
        recipient_manage,
        message_manage,
        status_get,
        message_send,
        reset,
        engine.die
    ]
    return _print_menu(name, options, actions)


def server_manage():
    """
    Function to handle first main menu point
    :return: A callable representing the action chosen in the mail server management menu.
    """
    name = "mail server connection management"
    options = [
        "View existing server configurations",
        "Add new server configuration",
        "Back to Main Menu"
    ]
    actions = [
        server_view_list,
        server_add,
        None
    ]
    return _print_menu(name, options, actions)


def _server_edit(server_list: ServerConnectionList, server: ServerConnection) -> None:
    """
    This inline function creates the editing menu for a server connections list entry
    :param server_list: The server list in which server resides (for purpose of deletion)
    :param server: The server to be edited.
    :return: None
    """
    if server not in server_list:
        return


def server_view_list():
    """
    This function displays a list of the existing server configurations.
    :return: None.
    """

    server_list = engine.server_connections_get_list()
    # List format:
    # 1. [Active] <Name>
    #        <smtp-host>:<smtp-name>, <encryption>
    #        <imap-host>:<imap-name>, <encryption>
    # 2. <Name>
    #        ...
    name = "server connections list"
    special_text = f"You are currently viewing the {name}.\nBy entering the number of one of the " \
                   f"entries, you choose this entry to perform changes to it.\nEditing is currently not supported and " \
                   f"results in return to main menu.\n"
    input_text = f"the number of the server you want to edit or {len(server_list) + 1} to exit this view"
    options: list[str] = []
    actions: list[Optional[Callable]] = []

    for server in server_list:
        option: str = f""
        if server == server_list.get_active():
            option += f"[Active] "
        option += f"{server.name}\n"
        option += f"\t{server.smtp['host']}:{server.smtp['port']}"
        if server.smtp["encryption"] is not False:
            option += f", {server.smtp['encryption'].name}"
        option += f"\n\t{server.imap['host']}:{server.imap['port']}"
        if server.imap["encryption"] is not False:
            option += f", {server.imap['encryption'].name}"
        options.append(option)
        # actions.append(lambda: _server_edit(server_list, server))
        actions.append(None)
        # TODO: implement the context menu function and remove the hint from list heading!

    options.append("Back to server connections management")
    actions.append(None)
    return _print_menu(name, options, actions, special_text=special_text, input_text=input_text)


def server_add():
    """
    This function provides the ui to add a new server configuration.
    :return:
    """
    num_steps = 11
    current_step = 1

    def _step_base(i: int) -> None:
        """
        This subfunction creates for every step of the process a clean screen and shows some basic information.
        :param i: the number of the current step.
        """
        _clear_screen()
        print(f"You are currently creating a new mail server connection configuration.\nStep {i} of {num_steps}\n")

    def _get_port(server_type: str) -> int | None:
        """
        This method asks for a port number and returns only an int, if the user enters a correct value.
        Else, and if the user aborts input, it returns None.
        :param server_type: A string containing some expression referring to a type of server.
        :return: the port number, if a valid one was entered by the user. None otherwise.
        """
        port: str = _create_input_message(f"{server_type} server port number")
        if _is_int(port):
            out: int = int(port)
            if out > 0:
                return out
        choice = input("Not a valid port number! Retry? (y/n) ")
        if choice.casefold() != "y":
            return None
        return _get_port(server_type)

    # Get SMTP host name
    _step_base(current_step)
    smtp_host = _create_input_message("SMTP server host name")
    if smtp_host.strip() == "":
        return None
    current_step += 1

    # Get SMTP port number
    _step_base(current_step)
    smtp_port = _get_port("SMTP")
    if smtp_port is None:
        return None
    current_step += 1

    # Ask if the SMTP server needs encryption, and if so, which one.
    _step_base(current_step)
    smtp_encryption = _get_pseudo_bool_option(
        "Does the SMTP server connection need to be encrypted?",
        [("No.", False), ("Yes, with SSL.", Encryption.SSL), ("Yes, with STARTTLS.", Encryption.STARTTLS)]
    )
    current_step += 1

    # Ask if the user needs to authenticate at the SMTP server.
    _step_base(current_step)
    smtp_login = _get_pseudo_bool_option(
        "Do you need to authenticate on the SMTP server in order to send mails?",
        [("Yes. [Credentials will be prompted on email sending]", True), ("No.", False)]
    )
    current_step += 1

    # Get IMAP host name
    _step_base(current_step)
    imap_host = _create_input_message("IMAP server host name")
    if imap_host.strip() == "":
        return None
    current_step += 1

    # Get IMAP port number
    _step_base(current_step)
    imap_port = _get_port("IMAP")
    if imap_port is None:
        return None
    current_step += 1

    # Ask if the IMAP server needs encryption, and if so, which one.
    _step_base(current_step)
    imap_encryption = _get_pseudo_bool_option(
        "Does the IMAP server connection need to be encrypted?",
        [("No.", False), ("Yes, with SSL.", Encryption.SSL), ("Yes, with STARTTLS.", Encryption.STARTTLS)]
    )
    current_step += 1

    # Ask if the user needs to authenticate at the IMAP server.
    _step_base(current_step)
    imap_login = _get_pseudo_bool_option(
        "Do you need to authenticate on the IMAP server?",
        [("Yes. [Credentials will be prompted on email sending]", True), ("No.", False)]
    )
    current_step += 1

    # Ask if the SMTP server and the IMAP server share authentication credentials.
    share_login: bool
    if smtp_login and imap_login:
        num_steps += 1
        _step_base(current_step)
        share_login = _get_pseudo_bool_option(
            "Do you use the same the same authentication credentials for SMTP server as for IMAP server?",
            [("Yes", True), ("No", False)]
        )
        current_step += 1
    else:
        share_login = False

    # Ask the user for its name for display as sender name
    # Ask the user for its email address for use in "From" field.
    _step_base(current_step)
    sender_name = _create_input_message("sender name for display in \"From\" field")
    sender_email = _create_input_message("sender email address for use in \"From\" field")
    if sender_name.strip() == "" or sender_email.strip() == "":
        return None
    current_step += 1

    # Get a name for this configuration
    _step_base(current_step)
    name = _create_input_message("an arbitrary name for this server connection configuration")
    if name.strip() == "":
        name = f"Server Config {time.time()}"
    current_step += 1

    # Ask if the new config shall serve immediately as active config.
    _step_base(current_step)
    active = _get_pseudo_bool_option(
        "Shall the new configuration serve immediately as the active one?",
        [("Yes.", True), ("No.", False)]
    )
    connection = ServerConnection(name, smtp_host, smtp_port, sender_name, sender_email, smtp_encryption, smtp_login,
                                  imap_host, imap_port, imap_encryption, imap_login, share_login)
    engine.server_connections_add_new(connection, active)


def recipient_view_list() -> None:
    """
    This function shows a list view of the recipients list.
    The context menu options are currently not available.
    :return: None.
    """
    recipients_list = engine.recipients_get_list()
    name = "recipients list"
    special_text = f"You are currently viewing the {name}.\nOf each recipient only the first email address is " \
                   f"shown.\nBy entering the number of one of the entries, you choose this entry to perform changes " \
                   f"to it.\nEditing is currently not supported and results in return to main menu.\n"
    input_text = f"the number of the recipient you want to edit or {len(recipients_list) + 1} to exit this view"
    options: list[str] = []
    actions: list[Optional[Callable]] = []

    for recipient in recipients_list:
        option: str = f"{recipient}"
        options.append(option)
        # actions.append(lambda: _recipient_edit(recipients_list, recipient))
        actions.append(None)
        # TODO: implement the context menu function and remove the hint from list heading!

    options.append("Back to recipients management")
    actions.append(None)
    return _print_menu(name, options, actions, special_text=special_text, input_text=input_text)


def recipient_add() -> None:
    """
    This function lets the user add a recipient to the list of recipients.
    :return: None
    """
    num_steps = 3
    current_step = 1

    def _step_base(i: int) -> None:
        """
        This subfunction creates for every step of the process a clean screen and shows some basic information.
        :param i: the number of the current step.
        """
        _clear_screen()
        print(f"You are currently adding a new recipient to your recipients list.\nStep {i} of {num_steps}\n")

    # Get recipient display name
    _step_base(current_step)
    name = _create_input_message("the recipient's name to display in \"To\" field")
    if name.strip() == "":
        return None
    current_step += 1

    # Get recipient email address
    _step_base(current_step)
    print(
        f"If you wish to add more than one email address for {name}, please enter now the main address and choose in the next screen to add more addresses.")
    address = _create_input_message(f"{name}'s email address for use in \"To\" field")
    if address.strip() == "":
        return None
    current_step += 1

    new_recipient: Recipient = Recipient(name, address)

    # Ask if there are more than one address to add to the recipient.
    _step_base(current_step)
    more = _get_pseudo_bool_option(
        f"Do you wish to add more than one email address for {name}?",
        [("Yes.", True), ("No.", False)]
    )

    # Add more email addresses
    while more:
        num_steps += 2
        current_step += 1
        _step_base(current_step)
        address = _create_input_message(f"{name}'s next email address for use in \"To\" field")
        if address.strip() == "":
            break
        new_recipient.add_address(address)
        current_step += 1

        _step_base(current_step)
        more = _get_pseudo_bool_option(
            f"Do you wish to add another email address for {name}?",
            [("Yes.", True), ("No.", False)]
        )
    engine.recipients_add_new(new_recipient)

    # Ask for more recipients
    _step_base(current_step)
    _get_pseudo_bool_option(
        f"Do you wish to add another recipient to the list?",
        [("Yes.", recipient_add), ("No.", lambda: None)]
    )()


def recipient_load_file() -> None:
    """
    This method loads a list of recipients from a file.
    There is currently one format accepted, although there might come more in the future.
    :return: None
    """
    _clear_screen()
    path: str = _create_input_message("the path to the file containing the recipients data")
    name: str = "recipients loading, part II"
    special_text: str = f"Loading file {path} ...\n\t"
    options: list[str] = ["Back to recipients management"]
    actions: list[Optional[Callable]] = [None]
    if engine.recipients_load_file(path):
        special_text += f"Recipients were successfully loaded!"
    else:
        special_text += f"Something went wrong. Please return to management menu to retry."
        # TODO: Have a more gentle way to retry!
    special_text += "\n"
    return _print_menu(name, options, actions, special_text=special_text)


def recipient_clear() -> None:
    """
    This function commands the engine to clear the recipients list.
    :return: None
    """
    engine.recipients_clear()


def recipient_manage():
    """
    Function to handle second main menu point
    :return: A callable representing the action chosen in the recipients management menu.
    """
    name: str = "mail recipients management"
    options: list[str] = [
        "View list of recipients",
        "Add new recipient",
        "Load recipients from file (Currently not implemented)",
        "Store recipients list into file (Currently not implemented)",
        "Clear recipients list",
        "Back to Main Menu"
    ]
    actions: list[Optional[Callable]] = [
        recipient_view_list,
        recipient_add,
        recipient_load_file,
        None,
        recipient_clear,
        None
    ]
    return _print_menu(name, options, actions)


def message_load():
    """
    This function handles the loading of a message from a disk file.
    :return: None
    """
    _clear_screen()
    path: str = _create_input_message("the path to the message file")
    name: str = "message loading, part II"
    special_text: str = f"Loading file {path} ...\n\t"
    options: list[str] = ["Back to mail message management"]
    actions: list[Optional[Callable]] = [None]
    if engine.message_load_file(path):
        special_text += f"Message was successfully loaded!"
    else:
        special_text += f"Something went wrong."
        options.insert(0, "Retry")
        actions.insert(0, message_load)
        # TODO: Stop the program from showing the "enter path" message twice after choosing "Retry"
    special_text += "\n"
    return _print_menu(name, options, actions, special_text=special_text)


def message_manage():
    """
    Function to handle third main menu point
    :return: A callable representing the action chosen in the mail message setup menu.
    """
    name: str = "mail message setup"
    options: list[str] = [
        "Write or modify a message here (currently not implemented)",
        "Load message from file",
        "Store message into file (currently not implemented)",
        "Clear message (currently not implemented)",
        "Back to Main Menu"
    ]
    actions: list[Optional[Callable]] = [None] * 5
    actions[1] = message_load
    return _print_menu(name, options, actions)


def status_get():
    """
    Function to handle fourth main menu point
    :return: A callable leading the application back to main menu.
    """
    name = ""
    options = [
        "Back to Main Menu"
    ]
    actions = [None]
    special_text = "Welcome to the status page.\nNot implemented yet.\n"
    return _print_menu(name, options, actions, special_text=special_text)


def message_send():
    """
    Function to handle fifth main menu point
    :return: A callable leading the application back to main menu.
    """

    def _message_send_2() -> None:
        """
        This function sends an email and shows, what happens.
        :return: None
        """

        def _exit() -> None:
            """
            This subfunction prints an exit message and returns.
            :return: None
            """
            input("Please press Enter to return to main menu ... ")

        name = None
        password = None
        server_connection = engine.server_connections_get_list().get_active()
        _clear_screen()
        print("Establishing connection ...\n")
        if server_connection is None:
            print("There is no active server connection!")
            return _exit()
        if server_connection.smtp["login"]:
            name = _create_input_message(f"user name for {server_connection.smtp['host']}")
            password = getpass(f"Please enter the password for {server_connection.smtp['host']}: ")
        status, result = engine.send_message(sys.stdout, smtp_user=name, smtp_password=password)
        _clear_screen()
        print(status)
        if result != "":
            print(result)
        return _exit()

    _clear_screen()
    print("Are you sure you want to send this email?\n\n1. Yes.\n2. No. Back to main menu.\n")

    input_text: str = "Are you sure you want to send this email?"
    choice = _create_input_message(input_text)
    while choice not in ("1", "2"):
        print("This is not a valid option!")
        choice = _create_input_message(input_text)
    match choice:
        case "1":
            return _message_send_2()
        case "2":
            return None


def reset():
    """
    Function to handle sixth main menu point
    :return: A callable leading the application back to main menu.
    """
    name = ""
    options = [
        "Yes.",
        "No. Back to Main Menu."
    ]
    actions = [None] * 2
    special_text = "Are you sure you want to delete everything within this application?"
    return _print_menu(name, options, actions, special_text=special_text)


class Parser(argparse.ArgumentParser):
    """
    This is a subclass that contains already some fixed configurations for this program.
    """

    def __init__(self):
        super().__init__(prog="bulk-mailer",
                         description="Send emails based on files to many recipients. All options can be set in config "
                                     "file and are thus optional.",
                         allow_abbrev=False
                         )
        self.add_argument("-m", "--message_file",
                          help="The path to a file containing an email message to send.")
        self.add_argument("-r", "--recipient",
                          action="extend",
                          nargs="+",
                          help="Adds a recipient to the message per call."
                          )

        self.add_argument("-rf", "--recipients_file",
                          help="The path to a file containing a list of recipients. If both r and rf are existent, "
                               "the recipients in the file in rf are simply appended to those in r.")
        self.add_argument("-c", "--config",
                          nargs="?",
                          default=argparse.SUPPRESS,
                          metavar="Key=Value",
                          help="Show config file, if no key/value pair is given, else set that key/value pair."
                          )
        self.add_argument("-v", "--verbose",
                          action="store_true",
                          help="Show more detailed output.")
        self.add_argument("-V", "--version",
                          action="version",
                          help="Show version information.",
                          version=CommandLine.headline
                          )
