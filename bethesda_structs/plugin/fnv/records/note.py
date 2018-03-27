# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from construct import *
from multidict import (CIMultiDict,)

from ._common import (
    FNV_ObjectBoundsStruct, FNV_FormID,
    FNV_ModelCollection,
)


FNV_NOTESubrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Enum(
        Int8ul,
        sound=0,
        text=1,
        image=2,
        voice=3
    ) * 'Type'),
    ('XNAM', CString('utf8') * 'Texture'),
    ('TNAM', CString('utf8') * 'Text / Topic'),
    ('SNAM', FNV_FormID(['SOUN', 'NPC_', 'CREA']) * 'Sound / Actor'),
], **FNV_ModelCollection)
