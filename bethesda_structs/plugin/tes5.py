# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import enum
import struct
import warnings
from typing import (List,)

from . import (tes4,)


class TES5Field(tes4.TES4Field):
    """ An object representing a TES5 field.
    """


class TES5Record(tes4.TES4Record):
    """ An object representing a TES5 record.
    """

    _prefix_struct = '<4sLLLHH'
    _prefix_names = (
        '_type', '_data_size', '_flags', '_form_id', '_vc', '_version',
        '_unknown_0',
    )

    class RecordFlags(enum.IntEnum):
        """ Available flags for TES5 record objects.
        """

        EMPTY = 0x00000000
        ESM = 0x00000001
        DELETED = 0x00000020
        CONSTANT = 0x00000040
        LOCALIZED = 0x00000080
        MUST_UPDATE_ANIMATIONS = 0x00000100
        CASTS_SHADOWS = 0x00000200
        PERSISTENT = 0x00000400
        INITIALLY_DISABLED = 0x00000800
        IGNORED = 0x00001000
        VISIBLE_WHEN_DISTANT = 0x00008000
        RANDOM_ANIMATION_START = 0x00010000
        DANGEROUS = 0x00020000
        DATA_COMPRESSED = 0x00040000
        CANT_WAIT = 0x00080000
        IGNORE_OBJECT_INTERACTION = 0x00100000
        IS_MARKER = 0x00800000
        OBSTACLE = 0x02000000
        NAVMESH_GEN_FILTER = 0x04000000
        NAVMESH_GEN_BOUNDINGBOX = 0x08000000
        MUST_EXIT_TO_TALK = 0x10000000
        CHILD_CAN_USE = 0x20000000
        NAVMESH_GEN_GROUND = 0x40000000
        MULTIBOUND = 0x80000000

    @property
    def fields(self) -> List[TES5Field]:
        """ The fields within the TES5 record.

        :getter: Discovers and returns the TES5 fields within the TES5 record
        :setter: Does not allow setting
        """

        if not hasattr(self, '_fields'):
            self._fields = []
            buffer_offset = 0
            while buffer_offset < self.data_size:
                field = TES5Field(self.data[buffer_offset:])
                buffer_offset += len(field)
                self._fields.append(field)
        return self._fields


class TES5Group(tes4.TES4Group):
    """ An object representing a TES5 group.
    """

    _prefix_struct = '<4sL4slHHHH'
    _prefix_names = (
        '_type', '_group_size', '_label', '_flags', '_datestamp',
        '_unknown_0', '_version', '_unknown_1',
    )


class TES5Plugin(tes4.TES4Plugin):
    """ Wrapper for a TES5 plugin.
    """

    def __init__(self, filepath: str):
        """ Initializes the TES5 plugin wrapper.

        :param filepath: The filepath for a given TES5 plugin
        :type filepath: str
        :returns: Does not return
        """

        warnings.warn((
            "TES5Plugin is currently experimental and will not work in "
            ".esps where CELL groups are used"
        ), UserWarning)
        super().__init__(filepath)

    @property
    def groups(self) -> List[TES5Group]:
        """ The groups contained within the TES5 plugin.

        :getter: Returns the list of groups within the TES5 plugin
        :setter: Does not allow setting
        """

        if not hasattr(self, '_groups'):
            self._groups = []
            buffer_offset = 0
            while buffer_offset < self.data_size:
                group = TES5Group(self.data[buffer_offset:])
                buffer_offset += len(group)
                self._groups.append(group)
        return self._groups

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a given filepath can be handled by this plugin.

        :param filepath: The filepath of a potential TES5 plugin
        :type filepath: str
        :returns: True if the plugin can handle it, otherwise False
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError((
                "no such file '{filepath}' exists"
            ).format(**locals()))
        with open(filepath, 'rb') as fp:
            try:
                header = tes4.TES4Record(fp.read(
                    struct.calcsize(tes4.TES4Record._prefix_struct)
                ))
                # should be able to handle the record if it's tagged as a TES4
                # and is version 131, hopefully...
                return (header.type == b'TES4') and (header.version == 131)
            except struct.error as exc:
                # catch if it can't even unpack the header
                pass
        return False
