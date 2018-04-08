# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
from typing import Any, Dict, List

import attr
from construct import Bytes, Struct, Int32ul

from .v103 import BSAArchive as v103_BSAArchive
from .v104 import BSAArchive as v104_BSAArchive
from .v105 import BSAArchive as v105_BSAArchive
from .._common import BaseArchive


class BSAArchive(BaseArchive):
    """Generic BSAArchive object factory.
    """

    generic_header = Struct("magic" / Bytes(4), "version" / Int32ul)
    factory_map = {103: v103_BSAArchive, 104: v104_BSAArchive, 105: v105_BSAArchive}

    def __new__(
        cls, content: bytes, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> object:
        """Object creation factory.

        Args:
            content (bytes): The content of an archive.

        Returns:
            object: Factory created object
        """

        header = cls.generic_header.parse(content)
        return cls.factory_map[header.version](content, *args, **kwargs)

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given filepath can be handled by a BSA archive.

        Args:
            filepath (str): The filepath to handle

        Returns:
            bool: True if the file can be handled, otherwise False
        """

        return any(
            bsa_archive.can_handle(filepath) for bsa_archive in cls.factory_map.values()
        )
