# coding=utf-8
"""
This file contains the routines that put the stuff in the lib package together to make a useful tool.

To cut things short: Here goes bulk-mailer execution file.
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
    number: int = 0
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