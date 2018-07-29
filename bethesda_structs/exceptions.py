# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://opensource.org/licenses/MIT>


class BethesdaStructsException(Exception):
    """A namespace for Bethesda structs exceptions.
    """

    def __init__(self, message: str, *args, **kwargs):
        """Initializes the exception.

        Args:
            message (str): The message of the exception
        """

        self.message = message
        super().__init__(message, *args, **kwargs)


class UnexpectedSubrecord(BethesdaStructsException):
    """A subrecord appeared where it wasn't expected
    """

    pass
