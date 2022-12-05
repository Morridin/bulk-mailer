# coding=utf-8
"""
This file holds all the stuff needed for a command line UI for the bulk mailer program.
"""
import argparse
import platform
import subprocess
from typing import Any, List, Callable, Union, Optional

import lib

HEADLINE = f"Bulk Mailer v{lib.__version__}"


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


def clear_screen():
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


def add_server():
    """
    This function provides the ui to add a new server configuration.
    :return:
    """
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


def die():
    """
    Function to handle seventh main menu point (exit the application).
    :return: None.
    """
    exit(0)
