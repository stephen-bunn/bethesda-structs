# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import io
import abc

from typing import (TypeVar, Generic,)

import attr
from construct import (Construct, Container, Subconstruct,)


T_BaseArchive = TypeVar('BaseArchive')


@attr.s
class BaseArchive(abc.ABC, Generic[T_BaseArchive]):
    """The base class all Archives should subclass.
    """

    content = attr.ib(type=bytes, repr=False)
    filepath = attr.ib(type=str, default=None)
    container = attr.ib(type=Container, default=None, repr=False, init=False)

    def __attrs_post_init__(self):
        self.container = self.archive_struct.parse(self.content)

    @abc.abstractproperty
    def archive_struct(self) -> Construct:
        """The base archive structure to use for parsing the archive.

        Returns:
            Construct: The archive structure
        """

        raise NotImplementedError

    @abc.abstractclassmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given `filepath` can be handled by the archive.

        Args:
            filepath (str): The filepath to evaluate

        Raises:
            NotImplementedError: Subclasses must define the logic

        Returns:
            bool: True if the `filepath` can be handled, otherwise False
        """

        raise NotImplementedError

    @classmethod
    def parse_bytes(
        cls,
        content: bytes,
        filepath: str=None
    ) -> T_BaseArchive:
        return cls(content, filepath=filepath)

    @classmethod
    def parse_stream(
        cls,
        stream: io.BufferedReader,
        filepath: str=None
    ) -> T_BaseArchive:
        return cls.parse_bytes(stream.read(), filepath=filepath)

    @classmethod
    def parse_file(cls, filepath: str) -> T_BaseArchive:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file '{filepath!r}' exists")
        with open(filepath, 'rb') as stream:
            return cls.parse_stream(stream, filepath)

    @abc.abstractmethod
    def extract(self, to_dir: str):
        raise NotImplementedError
