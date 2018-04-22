# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

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
        """
        raise NotImplementedError
