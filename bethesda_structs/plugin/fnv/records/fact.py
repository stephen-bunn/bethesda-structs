# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from construct import *
from multidict import (CIMultiDict,)

from ._common import (
    FNV_ObjectBoundsStruct, FNV_FormID,
    FNV_ModelCollection,
)


FNV_FACTSubrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('FULL', CString('utf8') * 'Name'),
    ('XNAM', Struct(
        "faction" / FNV_FormID(['FACT', 'RACE']),
        "modifier" / Int32sl,
        "group_combat_reaction" / Enum(
            Int32ul,
            neutral=0,
            enemy=1,
            ally=2,
            friend=3
        )
    ) * 'Relation'),
    ('DATA', Struct(
        "flags_1" / FlagsEnum(
            Int8ul,
            hidden_from_pc=0x01,
            evil=0x02,
            special_combat=0x04
        ),
        "flags_2" / FlagsEnum(
            Int8ul,
            track_crime=0x01,
            allow_sell=0x02
        ),
        "unused" / Byte[2]
    ) * 'Data'),
    ('CNAM', Float32l * 'Unused'),
    ('RNAM', Int32sl * 'Rank Number'),
    ('MNAM', CString('utf8') * 'Male'),
    ('FNAM', CString('utf8') * 'Female'),
    ('INAM', CString('utf8') * 'Insignia (unused)'),
    ('WMI1', FNV_FormID(['REPU']) * 'Reputation')
])
