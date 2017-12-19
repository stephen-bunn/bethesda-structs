# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import enum
import zlib
import struct
from typing import (List,)

from .. import (meta,)
from ._common import (AbstractPlugin,)


class TES4Field(meta.Prefixed):
    """ An object representing a TES4 field.
    """

    _prefix_struct = '<4sH'
    _prefix_names = ('_type', '_data_size',)

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} {self.type}>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the TES4 field in bytes.

        :returns: The length of the TES4 field in bytes
        """

        return (self._prefix_size + self.data_size)

    @property
    def type(self) -> bytes:
        """ The type of the TES4 field object.

        :getter: Returns the type TES4 field
        :setter: Does not allow setting
        """

        return self._type

    @property
    def data_size(self) -> int:
        """ The size in bytes of the TES4 field data.

        :getter: Returns the size in bytes of the TES4 field data
        :setter: Does not allow setting
        """

        return self._data_size

    @property
    def data(self) -> bytes:
        """ The data of the TES4 field.

        :getter: Returns the data of the TES4 field
        :setter: Does not allow setting
        """

        return self._buffer[
            self._prefix_size:(self._prefix_size + self.data_size)
        ]


class TES4Record(meta.Prefixed):
    """ An object representing a TES4 record.
    """

    _prefix_struct = '<4sLLLLL'
    _prefix_names = (
        '_type', '_data_size', '_flags', '_form_id', '_vc', '_version',
    )

    class RecordFlags(enum.IntEnum):
        """ Available flags for TES4 record objects.
        """

        EMPTY = 0x00000000
        ESM = 0x00000001
        DELETED = 0x00000020
        CASTS_SHADOWS = 0x00000200
        PERSISTENT = 0x00000400
        QUEST_ITEM = PERSISTENT
        INITIALLY_DISABLED = 0x00000800
        IGNORED = 0x00001000
        VISIBLE_WHEN_DISTANT = 0x00008000
        DANGEROUS = 0x00020000
        OFF_LIMITS = DANGEROUS
        DATA_COMPRESSED = 0x00040000
        CANT_WAIT = 0x00080000

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} {self.type} ({self.form_id})>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the TES4 record in bytes.

        :returns: The length of the TES4 record in bytes
        """

        return (self._prefix_size + self.data_size)

    @property
    def type(self) -> bytes:
        """ The type of the TES4 record object.

        :getter: Returns the type TES4 record
        :setter: Does not allow setting
        """

        return self._type

    @property
    def data_size(self) -> int:
        """ The size in bytes of the TES4 record data.

        :getter: Returns the size in bytes of the TES4 record data
        :setter: Does not allow setting
        """

        return self._data_size

    @property
    def vc(self) -> int:
        """ Version control information of the TES4 record.

        .. note:: I have no clue how to interpret this data 😞

        :getter: Returns the version control information of the TES4 record
        :setter: Does not allow setting
        """

        return self._vc

    @property
    def version(self) -> int:
        """ The format version of the TES4 record.

        :getter: Returns the format version of the TES4 record
        :setter: Does not allow setting
        """

        return self._version

    @property
    def form_id(self) -> str:
        """ The formatted form id as a padded hexidecimal string.

        .. note:: The integer value of this id can be accessed through \
            the "private" ``_form_id`` attribute.

        :getter: Returns the formatted form id as a padded hexidecimal string
        :setter: Does not allow setting
        """

        return ('{0:#0{1}x}').format(self._form_id, 0xa)

    @property
    def flags(self) -> RecordFlags:
        """ The record flags of the TES4 record.

        :getter: Returns the record flags of the TES4 record
        :setter: Does not allow setting
        """

        return self.RecordFlags(self._flags)

    @property
    def editor_id(self) -> bytes:
        """ The discovered editor id of the TES4 record.

        :getter: Discovers and returns the editor id of the TES4 record
        :setter: Does not allow setting
        """

        if not hasattr(self, '_editor_id'):
            self._editor_id = None
            # iterate over the extracted fields and see if one with type
            # EDID exists...
            for field in self.fields:
                if field.type == b'EDID':
                    self._editor_id = field.data
        return self._editor_id

    @property
    def data(self) -> bytes:
        """ The data of the TES4 record.

        .. note:: When :const:`flags.DATA_COMPRESSED` is true, \
            the record data is compressed and can be decompressed \
            with :mod:`zlib` using :const:`zlib.MAX_WBITS` as the \
            extraction method (`zlib`).\
            **This is done automatically.**

        :getter: Returns the data of the TES4 record
        :setter: Does not allow setting
        """

        # sometimes record data is compressed using zlib 6 something
        # this is indicated by the DATA_COMPRESSED flag
        if self.flags.DATA_COMPRESSED:
            if not hasattr(self, '_uncompressed_data'):
                try:
                    # try to decompress the data using zlib
                    self._uncompressed_data = zlib.decompress(
                        self._buffer[
                            (self._prefix_size + 0x4):
                            (self._prefix_size + self.data_size)
                        ],
                        zlib.MAX_WBITS
                    )
                    return self._uncompressed_data
                except zlib.error as exc:
                    # XXX: broken decoding has occured on some archives...
                    # most likely indicates incorrect plugin version such as
                    # TES3 or TES5
                    pass
        return self._buffer[
            self._prefix_size:(self._prefix_size + self.data_size)
        ]

    @property
    def fields(self) -> List[TES4Field]:
        """ The fields within the TES4 record.

        :getter: Discovers and returns the TES4 fields within the TES4 record
        :setter: Does not allow setting
        """

        if not hasattr(self, '_fields'):
            self._fields = []
            buffer_offset = 0
            while buffer_offset < self.data_size:
                field = TES4Field(self.data[buffer_offset:])
                buffer_offset += len(field)
                self._fields.append(field)
        return self._fields


class TES4Group(meta.Prefixed):
    """ An object representing a TES4 group.
    """

    _prefix_struct = '<4sL4slLL'
    _prefix_names = (
        '_type', '_group_size', '_label', '_flags', '_datestamp', '_version',
    )

    class GroupFlags(enum.IntEnum):
        """ Available flags for TES4 group objects.
        """

        TOP = 0x0
        WORLD_CHILDREN = 0x1
        INTERIOR_CELL_BLOCK = 0x2
        INTERIOR_CELL_SUBBLOCK = 0x3
        EXTERIOR_CELL_BLOCK = 0x4
        EXTERIOR_CELL_SUBBLOCK = 0x5
        CELL_CHILDREN = 0x6
        TOPIC_CHILDREN = 0x7
        CELL_PERSISTENT = 0x8
        CELL_TEMPORARY_CHILDREN = 0x9
        CELL_VISIBLE_DISTANT_CHILDREN = 0xa

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} ({self.flags}) {self.label}>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the TES4 record in bytes.

        :returns: The length of the TES4 record in bytes
        """

        return self.group_size

    @property
    def type(self) -> bytes:
        """ The type of the TES4 group object.

        .. note:: Should always be ``GRUP``.\
            If it isn't, I fucked up somewhere.

        :getter: Returns the type TES4 group
        :setter: Does not allow setting
        """

        return self._type

    @property
    def group_size(self) -> int:
        """ The size of the TES4 group in bytes.

        .. note:: Includes the bytes for the TES4 group's prefix.

        :getter: Returns the size of the TES4 group in bytes
        :setter: Does not allow setting
        """

        return self._group_size

    @property
    def label(self) -> bytes:
        """ The label of the TES4 group.

        :getter: Returns the label of the TES4 group
        :setter: Does not allow setting
        """

        return self._label

    @property
    def datestamp(self) -> int:
        """ The datestamp of the TES4 group.

        .. note:: I have no clue how to interpret this data 😞

        :getter: Returns the datestamp of the TES4 group
        :setter: Does not allow setting
        """

        return self._datestamp

    @property
    def version(self) -> int:
        """ The version of the TES4 group.

        :getter: Returns the version of the TES4 group
        :setter: Does not allow setting
        """

        return self._version

    @property
    def flags(self) -> GroupFlags:
        """ The flags of the TES4 group.

        :getter: Returns the flags of the TES4 group
        :setter: Does not allow setting
        """

        return self.GroupFlags(self._flags)

    @property
    def data_size(self) -> int:
        """ The size of the TES4 group data.

        :getter: Returns the size of the TES4 group data
        :setter: Does not allow setting
        """

        return (self.group_size - self._prefix_size)

    @property
    def data(self) -> bytes:
        """ The data of the TES4 group.

        :getter: Returns the data of the TES4 group
        :setter: Does not allow setting
        """

        return self._buffer[
            self._prefix_size:(self._prefix_size + self.data_size)
        ]

    @property
    def records(self) -> List[TES4Record]:
        """ The records within the TES4 group.

        :getter: Returns the list of records within the TES4 group
        :setter: Does not allow setting
        """

        if not hasattr(self, '_records'):
            self._records = []
            buffer_offset = 0
            while buffer_offset < self.data_size:
                record = TES4Record(self.data[buffer_offset:])
                buffer_offset += len(record)
                self._records.append(record)
        return self._records


class TES4Plugin(AbstractPlugin):
    """ Wrapper for a TES4 plugin.
    """

    def __init__(self, filepath: str):
        """ Initializes the TES4 plugin wrapper.

        :param filepath: The filepath for a given TES4 plugin
        :type filepath: str
        :returns: Does not return
        """

        self.filepath = filepath
        with open(self.filepath, 'rb') as fp:
            self._buffer = fp.read()
        self._header = TES4Record(self._buffer)

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} "{self.filepath}">'
        ).format(**locals())

    @property
    def filepath(self) -> str:
        """ The filepath of the TES4 plugin.

        :getter: Returns the filepath of the TES4 plugin
        :setter: Sets the filepath of the TES4 plugin
        """

        return self._filepath

    @filepath.setter
    def filepath(self, path: str) -> None:
        """ Sets the filepath of the TES4 plugin.

        :param path: The new filepath of the TES4 plugin
        :type path: str
        :returns: Does not return
        """

        if not os.path.isfile(path):
            raise FileNotFoundError((
                "no such file '{path}' exists"
            ).format(**locals()))
        self._filepath = path

    @property
    def header(self) -> TES4Record:
        """ The header of the TES4 plugin.

        :getter: Returns the header of the TES4 plugin
        :setter: Does not allow setting
        """

        return self._header

    @property
    def data_size(self) -> int:
        """ The size of the data after the header.

        :getter: Returns the size of the data after the header
        :setter: Does not allow setting
        """

        return len(self.data)

    @property
    def data(self) -> bytes:
        """ The data of the TES4 plugin, bytes after the header.

        :getter: Returns the bytes within the TES4 plugin, after the header
        :setter: Does not allow setting
        """

        return self._buffer[len(self.header):]

    @property
    def groups(self) -> List[TES4Group]:
        """ The groups contained within the TES4 plugin.

        :getter: Returns the list of groups within the TES4 plugin
        :setter: Does not allow setting
        """

        if not hasattr(self, '_groups'):
            self._groups = []
            buffer_offset = 0
            while buffer_offset < self.data_size:
                group = TES4Group(self.data[buffer_offset:])
                buffer_offset += len(group)
                self._groups.append(group)
        return self._groups

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a given filepath can be handled by this plugin.

        :param filepath: The filepath of a potential TES4 plugin
        :type filepath: str
        :returns: True if the plugin can handle it, otherwise False
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError((
                "no such file '{filepath}' exists"
            ).format(**locals()))
        with open(filepath, 'rb') as fp:
            try:
                header = TES4Record(fp.read(
                    struct.calcsize(TES4Record._prefix_struct)
                ))
                # should be able to handle the record if it's tagged as a TES4
                # and is version 43, hopefully...
                return (header.type == b'TES4') and (header.version == 43)
            except struct.error as exc:
                # catch if it can't even unpack the header
                pass
        return False
