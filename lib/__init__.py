# coding=utf-8
"""
This package contains all the mechanics of the whole project.
"""
__version__ = "0.0.1"

__all__ = ["commandline", "__version__", "server_connections", "recipients", "engine", "UI"]

from abc import abstractmethod, ABCMeta


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