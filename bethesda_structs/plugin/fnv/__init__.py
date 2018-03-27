# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

import os
from typing import (List, Generator,)

from construct import *

from .records import (FNV_SubrecordMap,)
from .records._common import (FNV_FormID,)
from .._common import (BasePlugin,)


class FNV_Plugin(BasePlugin):
    """ The plugin for Fallout: New Vegas.
    """

    subrecord_struct = Struct(
        "type" / PaddedString(4, 'utf8'),
        "data_size" / Int16ul,
        "data" / Bytes(lambda this: this.data_size),
        "parsed" / Computed(lambda this: FNV_Plugin._parse_fields(
            this.data,
            this.type,
            this._.parent
        ))
    ) * 'The subrecord structure for Fallout: New Vegas'

    record_struct = Struct(
        "type" / PaddedString(4, 'utf8'),
        "data_size" / Int32ul,
        "flags" / FlagsEnum(
            Int32ul,
            master=0x00000001,
            _unknown_0=0x00000002,  # NOTE: unknown flag
            _unknown_1=0x00000004,  # NOTE: unknown flag
            _unknown_2=0x00000008,  # NOTE: unknown flag
            form_initialized=0x00000010,
            deleted=0x00000020,
            constant=0x00000040,
            fire_disabled=0x00000080,
            inaccessible=0x00000100,
            casts_shadows=0x00000200,
            persistent=0x00000400,
            initially_disabled=0x00000800,
            ignored=0x00001000,
            no_voice_filter=0x00002000,
            cannot_save=0x00004000,
            visible_when_distant=0x00008000,
            random_anim_start=0x00010000,
            dangerous=0x00020000,
            compressed=0x00040000,
            cant_wait=0x00080000,
            _unknown_3=0x00100000,  # NOTE: unknown flag
            _unknown_4=0x00200000,  # NOTE: unknown flag
            _unknown_5=0x00400000,  # NOTE: unknown flag
            _unknown_6=0x00800000,  # NOTE: unknown flag
            destructible=0x01000000,
            obstacle=0x02000000,
            navmesh_filter=0x04000000,
            navmesh_box=0x08000000,
            non_pipboy=0x10000000,
            child_can_use=0x20000000,
            navmesh_ground=0x40000000,
            _unknown_7=0x80000000,  # NOTE: unknown flag
        ),
        "id" / Int32ul,
        "revision" / Int32ul,
        "version" / Int16ul,
        "_unknown_0" / Int16ul,
        If(lambda this: this.flags.compressed, Padding(Int32ul.sizeof())),
        "data" / IfThenElse(
            lambda this: this.flags.compressed,
            Compressed(GreedyBytes, 'zlib'),
            Bytes(lambda this: this.data_size)
        ),
        "subrecords" / Computed(lambda this: list(
            FNV_Plugin._parse_subrecords(this.data, this.type)
        ))
    ) * 'The record structure for Fallout: New Vegas'

    group_struct = Struct(
        "type" / Const(b'GRUP'),
        "group_size" / Int32ul,
        "_label" / Bytes(4), # NOTE: deferred  until group_type is determined
        "group_type" / Enum(
            Int32sl,
            top_level=0,
            world_children=1,
            interior_cell_block=2,
            interior_cell_subblock=3,
            exterior_cell_block=4,
            exterior_cell_subblock=5,
            cell_children=6,
            topic_children=7,
            cell_persistent_children=8,
            cell_temporary_children=9,
            cell_visible_distant_children=10
        ),
        "label" / Computed(lambda this: {
            'top_level': PaddedString(4, 'utf8'),
            'world_children': FNV_FormID(['WRLD']),
            'interior_cell_block': Int32sl,
            'interior_cell_subblock': Int32sl,
            'exterior_cell_block': Struct(
                Int16sl,
                "y" / Int8sl,
                "x" / Int8sl
            ),
            'exterior_cell_subblock': Struct(
                Int16sl,
                "y" / Int8sl,
                "x" / Int8sl
            ),
            'cell_children': FNV_FormID(['CELL']),
            'topic_children': FNV_FormID(['DIAL']),
            'cell_persistent_children': FNV_FormID(['CELL']),
            'cell_temporary_children': FNV_FormID(['CELL']),
            'cell_visible_distant_children': FNV_FormID(['CELL'])
        }[this.group_type].parse(this._label)),
        "stamp" / Int16ul,
        "unknown" / Bytes(6),
        "data" / Bytes(lambda this: this.group_size - 24),
        "records" / Computed(lambda this: list(
            FNV_Plugin._parse_records(this.data)
        ))
    ) * 'The group structure for Fallout: New Vegas'

    plugin_struct = Struct(
        "header" / record_struct,
        "groups" / GreedyRange(group_struct)
    ) * 'The plugin structure for Fallout: New Vegas'


    @property
    def plugin_structure(self) -> Struct:
        """ The base structure of the plugin.

        Returns:
            Struct: The base structure of the plugin
        """

        return self.plugin_struct

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a file can be handled by the plugin.

        Args:
            filepath (str): The filepath of the file to handle

        Raises:
            FileNotFoundError: If the given filepath doesn't exist

        Returns:
            bool: True if the file can be handled by the plugin
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file {filepath!r} exists")

        with open(filepath, 'rb') as stream:
            header = cls.record_struct.parse_stream(stream)
            return header.type == 'TES4' and header.version == 15

    @classmethod
    def _parse_fields(
        cls, subrecord_data: bytes, subrecord_type: str, record_type: str
    ) -> Generator[Container, None, None]:
        """ Parses fields from subrecord data.

        Args:
            subrecord_data (bytes): The data of the subrecord
            subrecord_type (str): The type of the subrecord
            record_type (str): The type of the record

        Returns:
            Generator[Container]: A list of Fields
        """

        if record_type in FNV_SubrecordMap:
            field_structure = FNV_SubrecordMap[record_type].get(
                subrecord_type,
                GreedyBytes
            )
            field = Container(
                value=field_structure.parse(subrecord_data),
                description=field_structure.docs
            )

            return field

    @classmethod
    def _parse_subrecords(
        cls, record_data: bytes, record_type: str
    ) -> Generator[Container, None, None]:
        """ Parses subrecords from record data.

        Args:
            record_data (bytes): The data of a record
            record_type (str): The type of a record

        Returns:
            List[Container]: A list of FNV_Subrecord
        """

        while record_data and len(record_data) > 0:
            subrecord = cls.subrecord_struct.parse(
                record_data,
                parent=record_type
            )
            record_data = record_data[(subrecord.data_size + 6):]

            yield subrecord

    @classmethod
    def _parse_records(
        cls, group_data: bytes
    ) -> Generator[Container, None, None]:
        """ Parses records from a group's data.

        Args:
            group_data (bytes): The data of a group

        Returns:
            Generator[Container]: A list of FNV_Record
        """

        while group_data and len(group_data) > 0:
            record = cls.record_struct.parse(group_data)
            group_data = group_data[(record.data_size + 24):]

            # register record in plugin's record registry
            cls.record_registry.add(record.type, record.id)

            yield record
