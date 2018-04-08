# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import io
import os
import abc
from typing import Generic, TypeVar, Callable, Generator
from pathlib import Path

import attr
from construct import Construct, Container, Subconstruct

from .._common import BaseFiletype


T_BaseArchive = TypeVar("BaseArchive")


@attr.s
class ArchiveFile(object):
    """An generic archive file object.
    """

    filepath = attr.ib(type=str, converter=Path)
    data = attr.ib(type=bytes, repr=False)

    @property
    def size(self) -> int:
        """int: The full size of the file.
        """
        return len(self.data)


@attr.s
class BaseArchive(BaseFiletype, abc.ABC, Generic[T_BaseArchive]):
    """The base class all Archives should subclass.
    """
    content = attr.ib(type=bytes, repr=False)
    filepath = attr.ib(type=str, default=None, converter=Path)
    container = attr.ib(type=Container, default=None, repr=False, init=False)

    def __attrs_post_init__(self):
        """Initializes the non-init attributes.
        """
        self.container = self.archive_struct.parse(self.content)

    @abc.abstractproperty
    def archive_struct(self) -> Construct:
        """The base archive structure to use for parsing the archive.

        Returns:
            Construct: The archive structure
        """
        raise NotImplementedError

    @classmethod
    def parse_bytes(cls, content: bytes, filepath: str = None) -> T_BaseArchive:
        """Create a `BaseArchive` from a byte array.

        Args:
            content (bytes): The byte content of the archive
            filepath (str, optional): Defaults to None. Sets the filepath attribute for
                user's reference

        Raises:
            ValueError: If the given content is not of bytes

        Returns:
            T_BaseArchive: A created `BaseArchive`
        """
        if not isinstance(content, bytes):
            raise ValueError(
                f"given content must be of bytes, recieved {type(content)!r}"
            )

        return cls(content, filepath=filepath)

    @classmethod
    def parse_stream(
        cls, stream: io.BufferedReader, filepath: str = None
    ) -> T_BaseArchive:
        """Create a `BaseArchive` from a file stream.

        Args:
            stream (io.BufferedReader): A file stream to read from.
            filepath (str, optional): Defaults to None. Sets the filepath attribute for
                user's reference.

        Raises:
            ValueError: If the given stream is not of ``bytes``

        Returns:
            T_BaseArchive: A created `BaseArchive`
        """
        if not isinstance(stream.peek(1), bytes):
            raise ValueError(
                f"stream {stream!r} is not a stream of bytes, recieved {type(stream)!r}"
            )

        return cls.parse_bytes(stream.read(), filepath=filepath)

    @classmethod
    def parse_file(cls, filepath: str) -> T_BaseArchive:
        """Create a `BaseArchive` from a given filepath.

        Args:
            filepath (str): The filepath to read from

        Raises:
            FileNotFoundError: If the given filepath does not exist

        Returns:
            T_BaseArchive: A created `BaseArchive`
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file {filepath!r} exists")

        with open(filepath, "rb") as stream:
            return cls.parse_stream(stream, filepath)

    @abc.abstractmethod
    def iter_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the available files in the archive.

        Yields:
            ArchiveFile: An archive file

        Raises:
            NotImplementedError: Subclasses must implement
        """
        raise NotImplementedError

    def extract(
        self, to_dir: str, progress_hook: Callable[[int, int, str], None] = None
    ):
        """Extracts the content of the `BaseArchive` to the given directory.

        Note:
            The provided progress hook is simple and two-stage. It is called once
            before a file is being written and once after the same file is done
            being written.

        Args:
            to_dir (str): The directory to extract the content to
            progress_hook (Callable[[int, int, str], None], optional): Defaults to None.
                A progress hook that should expect (``current``, ``total``,
                ``current_filepath``) as arguments
        """

        if not os.path.isdir(to_dir):
            raise NotADirectoryError(f"no directory {to_dir!r} exists")

        to_dir = Path(to_dir)

        archive_files = list(self.iter_files())
        total_size = sum(entry.size for entry in archive_files)
        current_size = 0

        for entry in archive_files:
            to_path = to_dir.joinpath(entry.filepath)
            if callable(progress_hook):
                progress_hook(current_size, total_size, to_path.as_posix())

            if not to_path.parent.is_dir():
                to_path.parent.mkdir(parents=True)
            with to_path.open("wb") as stream:
                stream.write(entry.data)
            current_size += entry.size

            if callable(progress_hook):
                progress_hook(current_size, total_size, to_path.as_posix())
