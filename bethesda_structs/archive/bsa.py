# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import struct
from typing import (List, Callable,)

from .. import (meta,)
from ._common import (AbstractArchive,)


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

        .. note:: Should always be ``BSA`` in bytes terminated by a null byte.

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

        # read the contents of the buffer into working memory
        # (kinda messy and stupid, just like me :D)
        self.filepath = filepath
        with open(self.filepath, 'rb') as fp:
            self._buffer = fp.read()

        # immediately build header since it's useful for pre-analysis before
        # extraction or processing of the data within the archive
        self._header = BSAHeader(self._buffer)

        # extract folders structs to a "private" variable because they
        # are not very useful to the user
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

    @property
    def files(self) -> List[BSAFile]:
        """ The files within the BSA archive.

        :getter: Discovers and returns the files within the BSA archive
        :setter: Does not allow setting
        """

        if not hasattr(self, '_files'):
            # oh jeez, here we go
            self._files = []

            # get the buffer offset for the begining of the file data,
            # this data is after both the archive prefix and all the folder
            # structures which were unpacked on initialization
            buffer_offset = (
                sum(len(folder) for folder in self._folders) +
                self.header._prefix_size
            )
            for folder in self._folders:

                # the length of the dirpath is stored in a single byte
                # preceeding the dirpath
                dirpath_length = ord(self._buffer[
                    buffer_offset:(buffer_offset + 1)
                ])
                # account for the byte that was just read
                buffer_offset += 1

                # get that damn dirpath
                dirpath = str(self._buffer[
                    buffer_offset:(buffer_offset + dirpath_length)
                ], 'utf-8')[:-1]
                # account for that damn dirpath
                buffer_offset += dirpath_length

                for _ in range(folder.file_count):
                    # each of the files within a folder take up a constant
                    # size in bytes (just their prefixes)
                    file_offset = struct.calcsize(BSAFile._prefix_struct)
                    # unpack and append the file given the **correct** buffer
                    file_ = BSAFile(
                        self._buffer[
                            buffer_offset:(buffer_offset + file_offset)
                        ],
                        dirpath
                    )
                    self._files.append(file_)
                    # account for the just unpacked file
                    buffer_offset += file_offset

            # now to get the bloody filenames
            # the filenames are in the same ordering as the file objects
            (file_idx, filename,) = (0, b'',)
            # there are no length indicators for filenames
            # so we just have to go until we hit a null terminator
            while file_idx < len(self._files):
                # get a character if a filename
                filename_char = self._buffer[buffer_offset:(buffer_offset + 1)]
                buffer_offset += 1
                # if its not the end of a filename (null terminator), continue
                if filename_char != b'\x00':
                    filename += filename_char
                    continue

                # add the built filename to the corresponding file object
                # (since they are ordered the same, just use index)
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
                # should be able to handle the archive if its tagged as a BSA
                return (header.bsa == b'BSA\x00')
            except struct.error as exc:
                # catch if it can't even unpack the header
                pass
        return False

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

        # ensure the parent directory exists before trying to write to it
        if not os.path.isdir(to_dir):
            raise NotADirectoryError((
                "no such directory '{to_dir}' exists"
            ).format(**locals()))

        total_count = len(self.files)
        for (file_idx, file_) in enumerate(self.files):
            # get the full path the file is going to be saved to
            to_path = os.path.join(to_dir, file_.filepath)
            file_dirpath = os.path.dirname(to_path)

            # if the full path's directory doesn't exist, create it
            if not os.path.isdir(file_dirpath):
                os.makedirs(file_dirpath)

            # if progress hook is enabled, report the progress
            if progress_hook:
                progress_hook((file_idx + 1), total_count, to_path)

            # write the archived file to the full path given the file
            # object's offset and size
            with open(to_path, 'wb') as fp:
                fp.write(self._buffer[
                    file_.offset:(file_.offset + file_.size)
                ])
