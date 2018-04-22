# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from ._common import BaseArchive
from .bsa import BSAArchive
from .btdx import BTDXArchive

AVAILABLE_ARCHIVES = (BSAArchive, BTDXArchive)


def get_archive(filepath: str) -> BaseArchive:
    """Get an instance of the first archive that can handle a given file.

    Args:
        filepath (str): The path of the file to handle

    Returns:
        BaseArchive: The base archive

    Examples:
        This method simply returns the first encountered archive that can handle a
        given file.

        >>> FILEPATH = ""  # absolute filepath to some BSA
        >>> archive = bethesda_structs.archive.get_archve(FILEPATH)
        >>> archive
        BSAArchive(filepath=PosixPath(...))
    """

    for arch in AVAILABLE_ARCHIVES:
        if arch.can_handle(filepath):
            return arch.parse_file(filepath)
