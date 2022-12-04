# bulk-mailer
A small Python tool to easily send e-mails in bulk to a group of recipients without showing all addresses to all recipients and without having to use the BCC field.

## Modules used (dependencies).

In order to keep things simple and the list of dependencies short, I'll try my best to only use standard lib modules.
Currently _planned_ for usage are 
* the `email` module to handle the message itself,
* the `smtplib` module to send messages,
* the `imaplib` module to catch any errors occuring when sending out the mails,
* the `configparser` module to handle configurations (maybe) and
* __later__ the `tk` modules to give a nice GUI. But that's something for a time far away.
* If necessary, the `ssl` module.


