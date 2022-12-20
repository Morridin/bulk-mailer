# coding=utf-8
"""
This file holds all the stuff needed for a command line UI for the bulk mailer program.
"""
import argparse
import platform
import subprocess
import time
from typing import Any, Callable, Union, Optional

import lib
from lib.server_connections import Encryption, ServerConnection, ServerConnectionList


SCL = ServerConnectionList()

class CommandLine(lib.UI):
    """
    This class bundles the interactive command line user interface.
    """
    headline = f"Bulk Mailer v{lib.__version__}"

    def __init__(self):
        self.command_stack: list[Callable] = [] # A stack containing the last menus called
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
        manage_connections,
        manage_recipients,
        manage_message,
        get_status,
        send_mail,
        reset,
        die
    ]
    return _print_menu(name, options, actions)


def _clear_screen():
    """
    This function clears the console screen.
    """
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear_screen"])


def _print_menu(menu_name: str,
                menu_options: list[str],
                menu_actions: list[Optional[Callable[[], Union[Callable, None]]]], *,
                special_text: str = None) -> Optional[Callable[[], Union[Callable, None]]]:
    """
    This function prints a menu and returns the choice of the user.
    :param menu_name: The name of the menu to print
    :param menu_options: The options in the menu to print
    :param menu_actions: The list of actions that correspond to
    the options in the menu.
    :param special_text: If the screen to show is no menu (or the "You are in menu X" text
    doesn't fit), use this parameter to hand in your own text.
    :return: The chosen action
    """
    clear_screen()
    print(HEADLINE)
    if special_text is None:
        print(f"""You are currently in the {menu_name}.
You have the following options:
""")
    else:
        print(special_text)

    actions: dict[str, Optional[Callable[[], Union[Callable, None]]]] = {}
    counter_width: int = len(str(len(menu_options)))

    for i, (option, action) in enumerate(zip(menu_options, menu_actions), 1):
        print(f"{i:>{counter_width}}. {option}")
        actions[f"{i}"] = action

    choice = input("\nPlease enter the number of the action you want to perform: ")
    while choice not in actions:
        print("This is not a valid option!")
        choice = input("Please enter the number of the action you want to perform: ")

    return actions[choice]





def manage_connections():
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
        view_server_list,
        add_server,
        None
    ]
    return _print_menu(name, options, actions)


def view_server_list():
    """
    This function displays a list of the existing server configurations.
    :return:
    """
    return None


def _create_input_message(item: str) -> str:
    """
    This function adds the value in item into a standard "Please enter X" input prompt and returns the input result.
    :param item: A textual description of what is expected.
    :return: The input of the user.
    """
    return input(f"Please enter {item}: ")


def is_int(s: str) -> int:
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


def add_server():
    """
    This function provides the ui to add a new server configuration.
    :return:
    """
    num_steps = 11
    current_step = 1

    def step_base(i: int) -> None:
        """
        This subfunction creates for every step of the process a clean screen and shows some basic information.
        :param i: the number of the current step.
        """
        clear_screen()
        print(HEADLINE)
        print(f"You are currently creating a new mail server connection configuration.\nStep {i} of {num_steps}\n")

    def _get_port(server_type: str) -> int | None:
        """
        This method asks for a port number and returns only an int, if the user enters a correct value.
        Else, and if the user aborts input, it returns None.
        :param server_type: A string containing some expression referring to a type of server.
        :return: the port number, if a valid one was entered by the user. None otherwise.
        """
        port: str = _create_input_message(f"{server_type} server port number")
        if is_int(port):
            out: int = int(port)
            if out > 0:
                return out
        choice = input("Not a valid port number! Retry? (y/n) ")
        if choice.casefold() != "y":
            return None
        return _get_port(server_type)

    def _get_pseudo_bool_option(question_text: str, options: list[tuple[str, Any]]) -> Any:
        """
        This subfunction asks the user a question and presents a set of answer options.
        It returns the value of the selected option.
        :param question_text: The text of the question to ask the user.
        :param options: A list consisting of tuples consisting of the displayed answers and their associated values.
        :return: the value of the selected option.
        """
        print(f"{question_text}\n")
        counter_width: int = len(str(len(options)))
        values: dict[str, Any] = {}
        for i, (option, value) in enumerate(options, 1):
            print(f"{i:>{counter_width}}. {option}")
            values[f"{i}"] = value
        choice = input("\nPlease enter the number of the best fitting option: ")
        while choice not in values:
            print("This is not a valid option!")
            choice = input("Please enter the number of the best fitting option: ")
        return values[choice]

    # Get SMTP host name
    step_base(current_step)
    smtp_host = _create_input_message("SMTP server host name")
    if smtp_host.strip() == "":
        return None
    current_step += 1

    # Get SMTP port number
    step_base(current_step)
    smtp_port = _get_port("SMTP")
    if smtp_port is None:
        return None
    current_step += 1

    # Ask if the SMTP server needs encryption, and if so, which one.
    step_base(current_step)
    smtp_encryption = _get_pseudo_bool_option(
        "Does the SMTP server connection need to be encrypted?",
        [("No.", False), ("Yes, with SSL.", Encryption.SSL), ("Yes, with STARTTLS.", Encryption.STARTTLS)]
    )
    current_step += 1

    # Ask if the user needs to authenticate at the SMTP server.
    step_base(current_step)
    smtp_login = _get_pseudo_bool_option(
        "Do you need to authenticate on the SMTP server in order to send mails?",
        [("Yes. [Credentials will be prompted on email sending]", True), ("No.", False)]
    )
    current_step += 1

    # Get IMAP host name
    step_base(current_step)
    imap_host = _create_input_message("IMAP server host name")
    if imap_host.strip() == "":
        return None
    current_step += 1

    # Get IMAP port number
    step_base(current_step)
    imap_port = _get_port("IMAP")
    if imap_port is None:
        return None
    current_step += 1

    # Ask if the IMAP server needs encryption, and if so, which one.
    step_base(current_step)
    imap_encryption = _get_pseudo_bool_option(
        "Does the IMAP server connection need to be encrypted?",
        [("No.", False), ("Yes, with SSL.", Encryption.SSL), ("Yes, with STARTTLS.", Encryption.STARTTLS)]
    )
    current_step += 1

    # Ask if the user needs to authenticate at the IMAP server.
    step_base(current_step)
    imap_login = _get_pseudo_bool_option(
        "Do you need to authenticate on the IMAP server?",
        [("Yes. [Credentials will be prompted on email sending]", True), ("No.", False)]
    )
    current_step += 1

    # Ask if the SMTP server and the IMAP server share authentication credentials.
    share_login: bool
    if smtp_login and imap_login:
        num_steps += 1
        step_base(current_step)
        share_login = _get_pseudo_bool_option(
            "Do you use the same the same authentication credentials for SMTP server as for IMAP server?",
            [("Yes", True), ("No", False)]
        )
        current_step += 1
    else:
        share_login = False

    # Ask the user for its name for display as sender name
    # Ask the user for its email address for use in "From" field.
    step_base(current_step)
    sender_name = _create_input_message("sender name for display in \"From\" field")
    sender_email = _create_input_message("sender email address for use in \"From\" field")
    if sender_name.strip() == "" or sender_email.strip() == "":
        return None
    current_step += 1

    # Get a name for this configuration
    step_base(current_step)
    name = _create_input_message("an arbitrary name for this server connection configuration")
    if name.strip() == "":
        name = f"Server Config {time.time()}"
    current_step += 1

    # Ask if the new config shall serve immediately as active config.
    step_base(current_step)
    active = _get_pseudo_bool_option(
        "Shall the new configuration serve immediately as the active one?",
        [("Yes.", True), ("No.", False)]
    )
    connection = ServerConnection(name, smtp_host, smtp_port, sender_name, sender_email, smtp_encryption, smtp_login,
                                  imap_host, imap_port, imap_encryption, imap_login, share_login)
    SCL.append(connection, active)
    return None


def manage_recipients():
    """
    Function to handle second main menu point
    :return: A callable representing the action chosen in the recipients management menu.
    """
    name = "mail recipients management"
    options = [
        "View list of recipients",
        "Add new recipient",
        "Load recipients from file",
        "Store recipients list into file",
        "Clear recipients list",
        "Back to Main Menu"
    ]
    actions = [None] * 6
    return _print_menu(name, options, actions)


def manage_message():
    """
    Function to handle third main menu point
    :return: A callable representing the action chosen in the mail message setup menu.
    """
    name = "mail message setup"
    options = [
        "Write or modify a message here",
        "Load message from file",
        "Store message into file",
        "Clear message",
        "Back to Main Menu"
    ]
    actions = [None] * 5
    return _print_menu(name, options, actions)


def get_status():
    """
    Function to handle fourth main menu point
    :return: A callable leading the application back to main menu.
    """
    name = ""
    options = [
        "Back to Main Menu"
    ]
    actions = [None]
    special_text = "Welcome to the status page."
    return _print_menu(name, options, actions, special_text=special_text)


def send_mail():
    """
    Function to handle fifth main menu point
    :return: A callable leading the application back to main menu.
    """
    name = ""
    options = [
        "Yes",
        "No. Back to Main Menu."
    ]
    actions = [None] * 2
    special_text = "Are you sure you want to send this email?"
    return _print_menu(name, options, actions, special_text=special_text)


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
                          version="Bulk Mailer 0.0"
                          )