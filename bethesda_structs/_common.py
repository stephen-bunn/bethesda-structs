# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

import io
import os
import abc
from typing import TypeVar

T_BaseFiletype = TypeVar("BaseFiletype")


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

    @abc.abstractclassmethod
    def parse(cls, content: bytes, filepath: str = None) -> T_BaseFiletype:
        """Create a :class:`BaseFiletype` from a byte array.

        Args:
            content (bytes): The byte content
            filepath (str, optional): Defaults to None.
                Sets the filepath attribute for user's reference

        Raises:
            NotImplementedError: Subclasses must implement

        Returns:
            :class:`BaseFiletype`: A filetype instance
        """
        raise NotImplementedError

    @classmethod
    def parse_stream(
        cls, stream: io.BufferedReader, filepath: str = None
    ) -> T_BaseFiletype:
        """Create a :class:`BaseFiletype` from a file stream.

        Args:
            stream (io.BufferedReader): A file stream to read from.
            filepath (str, optional): Defaults to None.
                Sets the filepath attribute for user's reference.

        Raises:
            ValueError: If the given stream is not of ``bytes``

        Returns:
            :class:`BaseFiletype`: A filetype instance
        """
        if not isinstance(stream.peek(1), bytes):
            raise ValueError(
                f"stream {stream!r} is not a stream of bytes, recieved {type(stream)!r}"
            )

        return cls.parse(stream.read(), filepath=filepath)

    @classmethod
    def parse_file(cls, filepath: str) -> T_BaseFiletype:
        """Create a :class:`BaseFiletype` from a given filepath.

        Args:
            filepath (str): The filepath to read from

        Raises:
            FileNotFoundError: If the given filepath does not exist

        Returns:
            :class:`BaseFiletype`: A filetype instance
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file {filepath!r} exists")

        with open(filepath, "rb") as stream:
            return cls.parse_stream(stream, filepath)
