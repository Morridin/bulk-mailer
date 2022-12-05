# coding=utf-8
"""
This file contains the routines that put the stuff in the lib package together to make a useful tool.

To cut things short: Here goes bulk-mailer execution file.
"""
import smtplib
from argparse import ArgumentParser

from lib import *

if __name__ == "__main__":
    parser: ArgumentParser = commandline.Parser()

    args = parser.parse_args()

    if args.verboose:
        print("Activated verboose output.")
        print(args)
