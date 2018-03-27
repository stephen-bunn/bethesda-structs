# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from construct import *
from multidict import (CIMultiDict,)


# XXX: missing OFST, DELE, SCRN, ONAM
FNV_TES4Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('HEDR', Struct(
        "version" / Float32l,
        "num_records" / Int32ul,
        "next_object_id" / Int32ul
    ) * 'Header'),
    ('CNAM', CString('utf8') * 'Author'),
    ('SNAM', CString('utf8') * 'Description'),
    ('MAST', CString('utf8') * 'Master'),
    ('DATA', Int64ul * 'File Size')
])
