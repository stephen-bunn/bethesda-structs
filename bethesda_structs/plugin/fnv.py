# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from construct import *


""" Fallout New Vegas subrecord structure.
Author: Stephen Bunn
Credit: TES5Edit Team <https://tes5edit.github.io/fopdoc/FalloutNV>
"""
FNVSubrecord = Struct(
    "type" / String(4, 'utf8'),
    "dataSize" / Int16ul,
    "data" / Bytes(lambda this: this.dataSize),
)


def _iter_subrecords(record_data: bytes):
    """ Greedy FNVSubrecord parser for FNVRecord data.

    :param bytes record_data: The data to parse FNVSubrecord(s) from
    :returns: A generator of FNVSubrecord(s)
    :rtype: generator[FNVSubrecord]
    """

    while record_data and len(record_data) > 0:
        subrecord = FNVSubrecord.parse(record_data)
        record_data = record_data[(subrecord.dataSize + 6):]
        yield subrecord


""" Fallout New Vegas record structure.
Author: Stephen Bunn
Credit: TES5Edit Team <https://tes5edit.github.io/fopdoc/FalloutNV>
"""
FNVRecord = Struct(
    "type" / String(4, 'utf8'),
    "dataSize" / Int32ul,
    "flags" / FlagsEnum(  # FIXME: find better names for these flags
        Int32ul,
        master=0x00000001,
        _unknown_0=0x00000002,  # NOTE: unknown flag
        _unknown_1=0x00000004,  # NOTE: unknown flag
        _unknown_2=0x00000008,  # NOTE: unknown flag
        form_initialized=0x00000010,
        deleted=0x00000020,
        border_region=0x00000040,
        turn_off_fire=0x00000080,
        inaccessible=0x00000100,
        cast_shadows=0x00000200,
        quest_item=0x00000400,
        initially_disabled=0x00000800,
        ignored=0x00001000,
        no_voice_filter=0x00002000,
        cannot_save=0x00004000,
        visible_when_distance=0x00008000,
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
    "id" / Bytes(4),
    "revision" / Int32ul,
    "version" / Int16ul,
    "unknown" / Int16ul,
    If(lambda this: this.flags.compressed, Padding(Int32ul.sizeof())),
    "data" / IfThenElse(
        lambda this: this.flags.compressed,
        Compressed(GreedyBytes, 'zlib'),
        Bytes(lambda this: this.dataSize)
    ),
    "subrecords" / Computed(lambda ctx: [
        entry
        for entry in _iter_subrecords(ctx.data)
    ])
)


def _iter_records(group_data: bytes):
    """ Greedy FNVRecord parser for FNVGroup data.

    :param bytes group_data: The data to parse FNVRecord(s) from
    :returns: A generator of FNVRecord(s)
    :rtype: generator[FNVRecord]
    """

    while group_data and len(group_data) > 0:
        record = FNVRecord.parse(group_data)
        group_data = group_data[(record.dataSize + 24):]
        yield record


""" Fallout New Vegas group structure.
Author: Stephen Bunn
Credit: TES5Edit Team <https://tes5edit.github.io/fopdoc/FalloutNV>
"""
FNVGroup = Struct(
    "type" / Const(b'GRUP'),
    "groupSize" / Int32ul,
    "label" / Bytes(4),
    "groupType" / Int32sl,
    "stamp" / Int16ul,
    "unknown" / Bytes(6),
    "data" / Bytes(lambda this: this.groupSize - 24),
    "records" / Computed(lambda ctx: [
        entry
        for entry in _iter_records(ctx.data)
    ]),
)


""" Fallout New Vegas plugin structure.
Author: Stephen Bunn
Credit: TES5Edit Team <https://tes5edit.github.io/fopdoc/FalloutNV>
"""
FNVPlugin = Struct(
    "header" / FNVRecord,
    "groups" / FNVGroup[:]
)
