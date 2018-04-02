# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import io
import abc

from construct import (Construct, Container,)


class BaseArchive(abc.ABC, Construct):
    """The base class all Archives should subclass.
    """

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

    def _parse(
        self,
        stream: io.BufferedReader,
        context: Container,
        path: str
    ) -> Container:
        """Parses the given stream using the archive struct.

        Args:
            stream (io.BufferedReader): The stream of bytes to parse
            context (Container): The contextual container to use
            path (str): The construct path

        Returns:
            Container: The resulting parsed container
        """

        return self.archive_struct._parse(stream, context, path)

    def _build(
        self,
        obj: Construct,
        stream: io.BufferedWriter,
        context: Container,
        path: str
    ) -> bytes:
        """Builds a given `obj` using the given `stream`.

        Args:
            obj (Construct): The construct to build
            stream (io.BufferedWriter): The stream to build the given `obj`
            context (Container): The contextual container to use
            path (str): The construct path

        Raises:
            NotImplementedError: Is not currently supported

        Returns:
            bytes: The resulting built bytes
        """

        raise NotImplementedError(
            f"{self!r} does not currently support building archives"
        )

    @abc.abstractmethod
    def extract(self, to_dir: str):
        raise NotImplementedError
