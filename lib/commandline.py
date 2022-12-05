# coding=utf-8
"""
This file holds all the stuff needed for a command line UI for the bulk mailer program.
"""
import argparse
import platform
import subprocess
from typing import Any, List, Callable

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


def _print_menu(menu_name: str, menu_options: list[str], menu_actions: list[Callable[[], None]]) -> Callable[[], None]:
    """
    This function prints a menu and returns the choice of the user.
    :param menu_name: The name of the menu to print
    :param menu_options: The options in the menu to print
    :param menu_actions: The list of actions that correspond to the options in the menu.
    :return: The chosen action
    """
    clear_screen()
    print(HEADLINE)
    print(f"""You are currently in the {menu_name}.
You have the following options:
""")
    actions: dict[str, Callable[[], None]] = {}
    counter_width: int = len(str(len(menu_options)))

    for i, (option, action) in enumerate(zip(menu_options, menu_actions), 1):
        print(f"{i:>{counter_width}}. {option}")
        actions[f"{i}"] = action

    choice = input("\nPlease enter the number of the action you want to perform: ")
    while choice not in actions:
        print("This is not a valid option!")
        choice = input("Please enter the number of the action you want to perform: ")

    return actions[choice]


def main_menu():
    """
    This function shows the main menu.
    :return: None
    """
    name: str = "main menu"
    options: list[str] = [
        "Manage Connections to mail servers",
        "Manage recipients list",
        "Manage email message",
        "Get current application status",
        "Send an email using the message, setup and recipients according to the current application status",
        "Reset the application",
        "Exit"
        ]
    actions: list[Callable[[], None]] = [
        manage_connections,
        manage_recipients,
        manage_message,
        get_status,
        send_mail,
        reset,
        die
    ]
    _print_menu(name, options, actions)()


def manage_connections():
    """
    Function to handle first main menu point
    :return:
    """
    name = "mail server connection management"
    options = []
    actions = []
    _print_menu(name, options, actions)()


def manage_recipients():
    """
    Function to handle second main menu point
    :return:
    """
    pass


def manage_message():
    """
    Function to handle third main menu point
    :return:
    """
    pass


def get_status():
    """
    Function to handle fourth main menu point
    :return:
    """
    pass


def send_mail():
    """
    Function to handle fifth main menu point
    :return:
    """
    pass


def reset():
    """
    Function to handle sixth main menu point
    :return:
    """
    pass


def die():
    """
    Function to handle seventh main menu point
    :return: None.
    """
    exit(0)
