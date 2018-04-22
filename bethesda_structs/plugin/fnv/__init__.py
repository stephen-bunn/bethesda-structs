# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

import io
import os
from typing import List, Generator

from construct import (
    If,
    Enum,
    Bytes,
    Const,
    Int8sl,
    Struct,
    Switch,
    Int16sl,
    Int16ul,
    Int32sl,
    Int32ul,
    Padding,
    Computed,
    Construct,
    Container,
    FlagsEnum,
    LazyBound,
    Compressed,
    IfThenElse,
    GreedyBytes,
    GreedyRange,
    PaddedString,
)
from multidict import CIMultiDict

from ._common import FNVFormID
from .records import RecordMapping
from .._common import BasePlugin


class FNVPlugin(BasePlugin):
    """The plugin for Fallout: New Vegas.

    This plugin structure *should* handle plugins for the games:
        - Fallout 3
        - Fallout: New Vegas

    Note:
        This structure *currently* reads all data on initialization.
        This may appear as *slower* initialization times for larger plugins.
        Should be fixed by
        `lazy constructs <https://construct.readthedocs.io/en/latest/lazy.html>`_
        when they become more stable.

    **Credit:**
        - `FopDoc <https://tes5edit.github.io/fopdoc/FalloutNV/Records.html>`_
    """

    subrecord_struct = Struct(
        "type" / PaddedString(4, "utf8"),
        "data_size" / Int16ul,
        "data" / Bytes(lambda this: this.data_size),
        "parsed"
        / Computed(
            lambda this: FNVPlugin.parse_subrecord(
                this._.id, this._.type, this.type, this.data
            )
        ),
    )
    """The structure for FO3/FNV subrecords.

    Returns:
        :class:`~construct.core.Struct`: The structure of FO3/FNV subrecords
    """

    record_struct = Struct(
        "type" / PaddedString(4, "utf8"),
        "data_size" / Int32ul,
        "flags"
        / FlagsEnum(
            Int32ul,
            master=0x00000001,
            _unknown_0=0x00000002,
            _unknown_1=0x00000004,
            _unknown_2=0x00000008,
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
            _unknown_3=0x00100000,
            _unknown_4=0x00200000,
            _unknown_5=0x00400000,
            _unknown_6=0x00800000,
            destructible=0x01000000,
            obstacle=0x02000000,
            navmesh_filter=0x04000000,
            navmesh_box=0x08000000,
            non_pipboy=0x10000000,
            child_can_use=0x20000000,
            navmesh_ground=0x40000000,
            _unknown_7=0x80000000,
        ),
        "id" / Int32ul,
        "revision" / Int32ul,
        "version" / Int16ul,
        "_unknown_0" / Int16ul,
        # NOTE: ignores compressed data size as it is handled by GreedyBytes
        If(lambda this: this.flags.compressed, Padding(4)),
        "data"
        / IfThenElse(
            lambda this: this.flags.compressed,
            Compressed(Bytes(lambda this: this.data_size), "zlib"),
            Bytes(lambda this: this.data_size),
        ),
        "subrecords"
        / Computed(
            lambda this: GreedyRange(FNVPlugin.subrecord_struct).parse(
                this.data, id=this.id, type=this.type
            )
        ),
    )
    """The structure for FO3/FNV records.

    Returns:
        :class:`~construct.core.Struct`: The structure of FO3/FNV records
    """

    # TODO: instead of using ``GreedyRange`` to handle parsing unknown length lists,
    # should probably use other repeaters to avoid messy construct debugging
    # (will always raise exception when expects record type to exist, but gets 0 bytes)
    group_struct = Struct(
        "type" / Const(b"GRUP"),
        "group_size" / Int32ul,
        # TODO: find a better way of lazily building ``label`` in place
        # instead of computing it later
        # NOTE: deferred until group_type is determined
        "_label" / Bytes(4),
        "group_type"
        / Enum(
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
            cell_visible_distant_children=10,
        ),
        "label"
        / Computed(
            lambda this: Switch(
                this.group_type,
                {
                    "top_level": PaddedString(4, "utf8"),
                    "world_children": FNVFormID(["WRLD"]),
                    "interior_cell_block": Int32sl,
                    "interior_cell_subblock": Int32sl,
                    "exterior_cell_block": Struct("y" / Int8sl, "x" / Int8sl),
                    "exterior_cell_subblock": Struct("y" / Int8sl, "x" / Int8sl),
                    "cell_children": FNVFormID(["CELL"]),
                    "topic_children": FNVFormID(["DIAL"]),
                    "cell_persistent_children": FNVFormID(["CELL"]),
                    "cell_temporary_children": FNVFormID(["CELL"]),
                    "cell_visible_distant_children": FNVFormID(["CELL"]),
                },
                default=GreedyBytes,
            ).parse(
                this._label
            )
        ),
        "stamp" / Int16ul,
        "_unknown_0" / Bytes(6),
        "data" / Bytes(lambda this: this.group_size - 24),
        "subgroups"
        / If(
            lambda this: (len(this.data) > 4 and this.data[:4] == b"GRUP"),
            Computed(
                lambda this: GreedyRange(
                    LazyBound(lambda: FNVPlugin.group_struct)
                ).parse(
                    this.data
                )
            ),
        ),
        "records"
        / If(
            lambda this: this.subgroups is None,
            Computed(
                lambda this: GreedyRange(FNVPlugin.record_struct).parse(this.data)
            ),
        ),
    )
    """The structure for FO3/FNV groups.

    Returns:
        :class:`~construct.core.Struct`: The structure of FO3/FNV groups
    """

    plugin_struct = Struct(
        "header" / record_struct * "Plugin header record",
        "groups" / GreedyRange(group_struct) * "Plugin groups",
    )
    """The structure for FO3/FNV plugins.

    Returns:
        :class:`~construct.core.Struct`: The structure of FO3/FNV plugins
    """

    # NOTE: working record is mangaled in order to protect state during
    # subrecord parsing for record state
    __working_record = {}

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given file can be handled by the plugin.

        Args:
            filepath (str): The filepath to evaluate

        Raises:
            FileNotFoundError: When the given `filepath` cannot be found

        Returns:
            bool: True if file can be handled, otherwise False
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"file {filepath!r} does not exist")

        header = cls.record_struct.parse_file(filepath)
        return header.type == "TES4" and header.version == 15

    @classmethod
    def parse_subrecord(
        cls,
        record_id: int,
        record_type: str,
        subrecord_type: str,
        subrecord_data: bytes,
    ) -> Container:
        """Parses a subrecord's data.

        Args:
            record_type (str): The parent record type
            subrecord_type (str): The subrecord type
            subrecord_data (bytes): The subrecord data to parse

        Returns:
            Container: The resulting parsed container
        """

        (record_type, subrecord_type) = (record_type.upper(), subrecord_type.upper())

        # handle reset of working record state
        if record_id not in cls.__working_record:
            cls.__working_record = {}
            cls.__working_record[record_id] = {}

        record_subrecords = RecordMapping.get(record_type)
        if record_subrecords:
            (parsed, working_record) = record_subrecords.handle_subrecord(
                subrecord_type, subrecord_data, cls.__working_record[record_id]
            )
            cls.__working_record[record_id] = working_record
            return parsed
