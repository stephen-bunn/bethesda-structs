# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from construct import *
from multidict import (CIMultiDict,)

from ._common import (
    FNV_ObjectBoundsStruct, FNV_FormID,
    FNV_ModelCollection, FNV_ItemCollection, FNV_DestructionCollection,
)


FNV_CONTSubrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('DATA', Struct(
        "flags" / FlagsEnum(
            Int8ul,
            _unknown_0=0x1,
            respawns=0x2
        ),
        "weight" / Float32l
    ) * 'Data'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Open'),
    ('QNAM', FNV_FormID(['SOUN']) * 'Sound - Close'),
    ('RNAM', FNV_FormID(['SOUN']) * 'Sound - Random / Looping'),
],
    **FNV_ModelCollection,
    **FNV_ItemCollection,
    **FNV_DestructionCollection
)
