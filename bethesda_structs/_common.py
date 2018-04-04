# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import abc


class BaseFiletype(abc.ABC):
    """The base filetype for all supported file parsers.
    """

    @abc.abstractclassmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given `filepath` can be handled by the archive.

        Args:
            filepath (str): The filepath to evaluate

        Raises:
            NotImplementedError: Subclasses must implement

        Returns:
            bool: True if the `filepath` can be handled, otherwise False
        """
        raise NotImplementedError
