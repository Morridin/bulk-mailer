# coding=utf-8
"""
This package bundles together the different UIs developed for bulk-mailer.
Currently there is only one, but there might come more.
"""

__all__ = ["UI", "commandline"]

from abc import ABCMeta, abstractmethod


class UI(metaclass=ABCMeta):
    """
    This is an abstract class defining some basic methods all valid user interfaces should have.
    """

    @abstractmethod
    def init(self, **kwargs) -> None:
        """
        This method is used to set up a user interface upon application start.
        """
        pass
