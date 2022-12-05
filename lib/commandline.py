# coding=utf-8
"""
This file holds all the stuff needed for a command line UI for the bulk mailer program.
"""
import argparse


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
        self.add_argument("-v", "--verboose",
                          action="store_true",
                          help="Show more detailed output.")
        self.add_argument("-V", "--version",
                          action="version",
                          help="Show version information.",
                          version="Bulk Mailer 0.0"
                          )
