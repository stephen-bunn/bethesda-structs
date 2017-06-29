#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT <https://opensource.org/licenses/MIT>

import os
import struct
from typing import (List, Callable,)

from .. import meta
from ._common import AbstractArchive


class BSAFile(meta.Prefixed):
    """ An object representing an archived BSA file.
    """

    _prefix_struct = '<QLL'
    _prefix_names = ('_hash', '_size', '_offset',)

    def __init__(self, buffer: bytes, dirpath: str):
        """ Initializes the BSA file object.

        :param buffer: The archive buffer starting at the file object offset
        :type buffer: bytes
        :param dirpath: The parent folder path of the BSA file
        :type dirpath: str
        """

        super().__init__(buffer)
        self._dirpath = os.path.normpath(dirpath).strip('.')

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} "{self.filepath}" '
            '({self.size} bytes)>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the BSA file in bytes.

        :returns: The length of the BSA file in bytes
        """

        return self.size

    @property
    def hash(self):
        """ A unique hash for the file object in the archive.

        :getter: Returns a unique hash for the file object in the archive
        :setter: Does not allow setting
        """

        return self._hash

    @property
    def size(self):
        """ The size of the archived file in bytes.

        :getter: Returns the size of the archived file in bytes
        :setter: Does not allow setting
        """

        return self._size

    @property
    def offset(self):
        """ The byte offset where the file object ends.

        :getter: Returns the byte offset where the file object ends
        :setter: Does not allow setting
        """

        return self._offset

    @property
    def filename(self) -> str:
        """ The filename of the BSA file.

        :getter: Returns the filename of the BSA file
        :setter: Does not allow setting
        """

        if not hasattr(self, '_filename'):
            self._filename = ''
        return self._filename

    @property
    def filepath(self) -> str:
        """ The archived filepath of the BSA file.

        :getter: Returns the archived filepath of the BSA file
        :setter: Does not allow setting
        """

        return os.path.join(self._dirpath, self.filename)


class BSAFolder(meta.Prefixed):
    """ An object representing an archived BSA folder.
    """

    _prefix_struct = '<QLL'
    _prefix_names = ('_hash', '_file_count', '_offset',)

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} ({self.file_count} files)>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the BSA folder prefix in bytes.

        :returns: The length of the BSA folder prefix in bytes
        """

        return self._prefix_size

    @property
    def hash(self):
        """ A unique hash for the folder object in the archive.

        :getter: Returns a unique hash for the folder object in the archive
        :setter: Does not allow setting
        """

        return self._hash

    @property
    def file_count(self):
        """ The number of files the folder contains.

        :getter: Returns the number of files the folder contains
        :setter: Does not allow setting
        """

        return self._file_count

    @property
    def offset(self):
        """ The byte offset where the folder object ends.

        :getter: Returns the byte offset where the folder object ends
        :setter: Does not allow setting
        """

        return self._offset


class BSAHeader(meta.Prefixed):
    """ An object representing an archived BSA header.
    """

    _prefix_struct = '<4sLLLLLLLL'
    _prefix_names = (
        '_bsa', '_version', '_offset', '_flags',
        '_folder_count', '_file_count',
        '_folder_names_length', '_file_names_length',
        '_other_flags',
    )

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} {self.bsa}>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the BSA header prefix in bytes.

        :returns: The length of the BSA header prefix in bytes
        """

        return self._prefix_size

    @property
    def bsa(self) -> bytes:
        """ The BSA magic of the header.

        :getter: Returns the BSA magic of the header
        :setter: Does not allow setting
        """

        return self._bsa

    @property
    def version(self) -> int:
        """ The version of the BSA archive format.

        :getter: Returns the version of the BSA archive format
        :setter: Does not allow setting
        """

        return self._version

    @property
    def offset(self) -> int:
        """ The byte offset where the BSA header ends.

        :getter: Returns the byte offset where the BSA header ends
        :setter: Does not allow setting
        """

        return self._offset

    @property
    def flags(self) -> int:
        """ Primary flags of the BSA archive.

        :getter: Returns primary flags of the BSA archive
        :setter: Does not allow setting
        """

        return self._flags

    @property
    def folder_count(self) -> int:
        """ The number of folders in the BSA archive.

        :getter: Returns the number of folders in the BSA archive
        :setter: Does not allow setting
        """

        return self._folder_count

    @property
    def file_count(self) -> int:
        """ The number of files in the BSA archive.

        :getter: Returns the number of files in the BSA archive
        :setter: Does not allow setting
        """

        return self._file_count

    @property
    def folder_names_length(self) -> int:
        """ The maximum length of a folder name in the BSA archive.

        :getter: Returns the maximum length of a folder name in the BSA archive
        :setter: Does not allow setting
        """

        return self._folder_names_length

    @property
    def file_names_length(self) -> int:
        """ The maximum length of a file name in the BSA archive.

        :getter: Returns the maximum length of a file name in the BSA archive
        :setter: Does not allow setting
        """

        return self._file_names_length

    @property
    def other_flags(self) -> int:
        """ Secondary flags of the BSA archive.

        :getter: Returns secondary flags of the BSA archive
        :setter: Does not allow setting
        """

        return self._other_flags


class BSAArchive(AbstractArchive):
    """ Wrapper for a BSA archive.
    """

    def __init__(self, filepath: str):
        """ Initializes the BSA archive wrapper.

        :param filepath: The filepath for a given BSA archive
        :type filepath: str
        :returns: Does not return
        """

        self.filepath = filepath
        with open(self.filepath, 'rb') as fp:
            self._buffer = fp.read()

        self.header = BSAHeader(self._buffer)

        self._folders = []
        buffer_offset = len(self.header)
        for _ in range(self.header.folder_count):
            folder = BSAFolder(self._buffer[buffer_offset:])
            buffer_offset += len(folder)
            self._folders.append(folder)

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} "{self.filepath}" '
            '({self.header.file_count} files)>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the number of files in the BSA archive.

        :returns: The number of fiels in the BSA archive
        """

        return self.header.file_count

    @property
    def filepath(self) -> str:
        """ The filepath of the BSA archive.

        :getter: Returns the filepath of the BSA archive
        :setter: Sets the filepath of the BSA archive
        """

        return self._filepath

    @filepath.setter
    def filepath(self, path: str) -> None:
        """ Sets the filepath of the BSA archive.

        :param path: The new filepath of the BSA archive
        :type path: str
        :returns: Does not return
        """

        if not os.path.isfile(path):
            raise FileNotFoundError((
                "no such file '{path}' exists"
            ).format(**locals()))
        self._filepath = path

    @property
    def header(self) -> BSAHeader:
        """ The header of the BSA archive.

        :getter: Returns the header of the BSA archive
        :setter: Sets the header of the BSA archive
        """

        return self._header

    @header.setter
    def header(self, header: BSAHeader) -> None:
        """ Sets the header of the BSA archive.

        :param header: The new header of the BSA archive
        :type header: BSAHeader
        :returns: Does not return
        """

        if not isinstance(header, BSAHeader):
            raise ValueError((
                "{self.__class__.__name__} header must be an instance of "
                "BSAHeader"
            ).format(**locals()))
        self._header = header

    @property
    def files(self) -> List[BSAFile]:
        """ The files within the BSA archive.

        :getter: Discovers and returns the files within the BSA archive
        :setter: Does not allow setting
        """

        if not hasattr(self, '_files'):
            self._files = []
            buffer_offset = (
                sum(len(folder) for folder in self._folders) +
                self.header._prefix_size
            )
            for folder in self._folders:
                filepath_length = ord(self._buffer[
                    buffer_offset:(buffer_offset + 1)
                ])
                buffer_offset += 1
                filepath = str(self._buffer[
                    buffer_offset:(buffer_offset + filepath_length)
                ], 'utf-8')[:-1]
                buffer_offset += filepath_length

                for _ in range(folder.file_count):
                    file_offset = struct.calcsize(BSAFile._prefix_struct)
                    file_ = BSAFile(
                        self._buffer[
                            buffer_offset:(buffer_offset + file_offset)
                        ],
                        filepath
                    )
                    self._files.append(file_)
                    buffer_offset += file_offset

            (file_idx, filename,) = (0, b'',)
            while file_idx < len(self._files):
                filename_char = self._buffer[buffer_offset:(buffer_offset + 1)]
                buffer_offset += 1
                if filename_char != b'\x00':
                    filename += filename_char
                    continue

                self._files[file_idx]._filename = str(filename, 'utf-8')
                filename = b''
                file_idx += 1

        return self._files

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a given filepath can be handled by this archive.

        :param filepath: The filepath of a potential BSA archive
        :type filepath: str
        :returns: True if the archive can handle it, otherwise False
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError((
                "no such file '{filepath}' exists"
            ).format(**locals()))
        with open(filepath, 'rb') as fp:
            try:
                header = BSAHeader(fp.read(
                    struct.calcsize(BSAHeader._prefix_struct)
                ))
                return (header.bsa == b'BSA\x00')
            except IndexError as exc:
                pass
        return False

    def extract(
        self,
        to_dir: str,
        hook: Callable[[int, int, str], None]=None
    ) -> None:
        """ Extracts the contents of the archive to a given directory.

        :param to_dir: The directory to extract files to
        :type to_dir: str
        :param hook: A progress hook for the extraction process
        :type hook: typing.Callable[[int, int, str], None]
        :returns: Does not return
        """

        if not os.path.isdir(to_dir):
            raise NotADirectoryError((
                "no such directory '{to_dir}' exists"
            ).format(**locals()))
        total_count = len(self.files)
        for (file_idx, file_) in enumerate(self.files):
            to_path = os.path.join(to_dir, file_.filepath)
            file_dirpath = os.path.dirname(to_path)
            if not os.path.isdir(file_dirpath):
                os.makedirs(file_dirpath)
            if hook:
                hook((file_idx + 1), total_count, to_path)
            with open(to_path, 'wb') as fp:
                fp.write(self._buffer[
                    file_.offset:(file_.offset + file_.size)
                ])
