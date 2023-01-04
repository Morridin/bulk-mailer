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
        * Load from file (later)
        * Store into file (later)
        * Clear ("Are you sure?")
    * Set up email message (either by writing it directly in the program or by importing a file containing the message)
        * Write here/modify (later)
        * Load from file
        * Store into file (later)
        * Clear
    * Get status (show current email message, recipients, selected server setup)
    * Send email to recipients => show overview of action about to be started and let user confirm this.
    * Reset application
    * Exit
"""
from lib import engine
from lib.ui.commandline import CommandLine

if __name__ == "__main__":
    interface = CommandLine()
    engine.init(interface)
