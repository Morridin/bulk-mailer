# coding=utf-8
"""
This file contains the routines that put the stuff in the lib package together to make a useful tool.

To cut things short: Here goes bulk-mailer execution file.

Wanted program flow:
* User starts program without parameters.
* Program shows a list of available actions and prompts for the wanted action
  This list should include:
    * Manage server connections
        * View existing
            * For each entry:
                * Change settings
                * Set as active (=currently used setup)
                * Delete
        * Add new
            1. Enter SMTP server host name
            2. Enter SMTP server port
            3. Enter, if SMTP server needs encryption
                * Enter, which type of encryption is necessary
            4. Enter, if SMTP server needs login
                * Choose between prompt on send or store persistent (unsafe)
            5. Enter IMAP server host name
            6. Enter IMAP server port
            7. Enter, if IMAP server needs encryption
                * Enter, which one.
            8. Enter login data or say "use SMTP data"
            9. Enter sender information ("From" field)
                1. Enter sender name
                2. Enter sender email address
            10. Enter name for that server connection setup ("Save as")
            11. Set as active?
    * Manage recipients
        * View list
            * For each entry:
                * Change
                * Delete
        * Add new
            1. Enter recipient name
            2. Enter recipient address
            3. More e-mail addresses for this recipient?
        * Load from file
        * Store into file
        * Clear ("Are you sure?")
    * Set up email message (either by writing it directly in the program or by importing a file containing the message)
        * Write here/modify
        * Load from file
        * Store into file
        * Clear
    * Get status (show current email message, recipients, selected server setup)
    * Send email to recipients => show overview of action about to be started and let user confirm this.
    * Reset application
    * Exit
"""
from argparse import ArgumentParser
from smtplib import SMTP

from lib import *


def get_int(*, input_text: str = "Enter number ", error_text: str = "Input is no valid number.",
            success_text: str = None, retry_text: str = "Retry? (y/n) ") -> int:
    """
    This function offers a way to safely get a number out of keyboard input.
    @param input_text: A message displayed on the input prompt
    @param error_text: A message displayed, when the input value is not a valid number
    @param success_text: An optional message displayed when the input was a valid number.
    @param retry_text: A message displayed upon erroneous input in order to restart the input.
    @return: The input int value, if any.
    """
    number_raw: str = input(input_text)
    try:
        number = int(number_raw)
    except ValueError:
        print(error_text)
        retry: str = input(retry_text)
        if retry.casefold() == "y".casefold():
            return get_int(input_text=input_text, error_text=error_text, success_text=success_text,
                           retry_text=retry_text)
        else:
            raise IOError()
    if success_text is not None:
        print(success_text)
    return number


if __name__ == "__main__":
    parser: ArgumentParser = commandline.Parser()
    args = parser.parse_args()

    if args.verboose:
        print("Activated verboose output.")
        print(args)

    host: str = input("SMTP server name ")
    port: int = get_int(input_text="SMTP server port ", error_text="Illegal Value for SMTP server port!")
    tls: bool = True

    with SMTP(host, port) as smtp:
        if tls:
            answer = smtp.starttls()
            print(answer)