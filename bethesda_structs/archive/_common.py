# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

import io
import os
import abc
from typing import Generic, TypeVar, Callable, Generator
from pathlib import Path

import attr
from construct import Construct, Container, StreamError

from .._common import BaseFiletype

T_BaseArchive = TypeVar("BaseArchive")


@attr.s
class ArchiveFile(object):
    """A generic archive file object that can be used for extracting.

    The purpose of this object is to provide some generic format for
    :func:`~BaseArchive.iter_files` to yield so that the :func:`~BaseArchive.extract`
    method can be abstracted away from the archive subclasses.
    """

    filepath = attr.ib(type=str, converter=Path)
    """The relative filepath of the archived file.

    Returns:
        str: The relative filepath of the archived file
    """

    data = attr.ib(type=bytes, repr=False)
    """The raw data of the archived file.

    Returns:
        bytes: The raw data of the archived file
    """

    @property
    def size(self) -> int:
        """The size of the raw data.

        Returns:
            int: The size of the raw data
        """
        return len(self.data)


@attr.s
class BaseArchive(BaseFiletype, abc.ABC, Generic[T_BaseArchive]):
    """The base class all Archives should subclass.
    """
    content = attr.ib(type=bytes, repr=False)
    filepath = attr.ib(type=str, default=None)
    container = attr.ib(type=Container, default=None, repr=False, init=False)

    def __attrs_post_init__(self):
        """Initializes the non-init attributes.
        """
        if self.filepath:
            self.filepath = Path(self.filepath)

        try:
            self.container = self.archive_struct.parse(self.content)
        except StreamError as exc:
            raise ValueError(
                (
                    f"parsing {self.__class__.__name__} archive struct is not large "
                    f"enough, {exc}"
                )
            )

    @abc.abstractproperty
    def archive_struct(self) -> Construct:
        """The base archive structure to use for parsing the **full** archive.

        Raises:
            NotImplementedError: Subclasses must implement

        Returns:
            :class:`construct.Construct`: The archive structure
        """
        raise NotImplementedError

    @classmethod
    def parse(cls, content: bytes, filepath: str = None) -> T_BaseArchive:
        """Create a :class:`BaseArchive` from a byte array.

        Args:
            content (bytes): The byte content of the archive
            filepath (str, optional): Defaults to None.
                Sets the filepath attribute for user's reference

        Raises:
            ValueError: If the given content is not of bytes

        Returns:
            :class:`BaseArchive`: An archive instance
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
        """Create a :class:`BaseArchive` from a file stream.

        Args:
            stream (io.BufferedReader): A file stream to read from.
            filepath (str, optional): Defaults to None.
                Sets the filepath attribute for user's reference.

        Raises:
            ValueError: If the given stream is not of ``bytes``

        Returns:
            :class:`BaseArchive`: An archive instance
        """
        if not isinstance(stream.peek(1), bytes):
            raise ValueError(
                f"stream {stream!r} is not a stream of bytes, recieved {type(stream)!r}"
            )

        return cls.parse(stream.read(), filepath=filepath)

    @classmethod
    def parse_file(cls, filepath: str) -> T_BaseArchive:
        """Create a :class:`BaseArchive` from a given filepath.

        Args:
            filepath (str): The filepath to read from

        Raises:
            FileNotFoundError: If the given filepath does not exist

        Returns:
            :class:`BaseArchive`: An archive instance
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

        Args:
            to_dir (str): The directory to extract the content to
            progress_hook (Callable[[int, int, str], None], optional): Defaults to None.
                A progress hook that should expect (``current``, ``total``,
                ``current_filepath``) as arguments

        Example:
            >>> FILEPATH = ""  # absolute path to BSA/BTDX archive
            >>> archive = bethesda_structs.archive.get_archive(FILEPATH)
            >>> archive.extract('/home/username/Downloads/extracted')

        Example:
            >>> def progress_hook(current, total, filepath):
            ...     print((current / total) * 100.0)
            >>> FILEPATH = ""  # absolute path to BSA/BTDX archive
            >>> archive = bethesda_structs.archive.get_archive(FILEPATH)
            >>> archive.extract(
            ...     '/home/username/Downloads/extracted',
            ...     progress_hook=progress_hook
            ... )
            0.0
            12.2
            12.2
            12.67
            12.67
            50.4443
            50.4443
            70.0
            70.0
            92.1
            92.1
            100.0

        Note:
            The provided progress hook is simple and two-stage. It is called once
            before a file is being written and once after the same file is done
            being written.
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
