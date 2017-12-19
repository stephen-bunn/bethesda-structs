# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import abc
from typing import (Callable,)

from .. import (meta,)


class AbstractArchive(meta.CheckSummed, metaclass=abc.ABCMeta):
    """ A template class for all archive structures.
    """

    def __eq__(self, other) -> bool:
        """ Evaluates if two archives are equal.

        :param other: Another AbstractArchive instance
        :type other: AbstractArchive
        :returns: True if equal, otherwise False
        """

        return self.checksum() == other.checksum()

    @classmethod
    @abc.abstractmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a given filepath can be handled by this archive.

        :param filepath: The filepath of a potential archive
        :type filepath: str
        :returns: True if the archive can handle it, otherwise False
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def extract(
        self,
        to_dir: str,
        progress_hook: Callable[[int, int, str], None]=None
    ) -> None:
        """ Extracts the contents of the archive to a given directory.

        :param to_dir: The directory to extract files to
        :type to_dir: str
        :param progress_hook: A progress hook for the extraction process
        :type progress_hook: typing.Callable[[int, int, str], None]
        :returns: Does not return
        """

        raise NotImplementedError()
