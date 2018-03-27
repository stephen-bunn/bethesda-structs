# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

from .tes4 import (FNV_TES4Subrecords,)
from .cont import (FNV_CONTSubrecords,)
from .note import (FNV_NOTESubrecords,)
from .fact import (FNV_FACTSubrecords,)

from multidict import (CIMultiDict,)


FNV_SubrecordMap = CIMultiDict({
    'TES4': FNV_TES4Subrecords,
    'CONT': FNV_CONTSubrecords,
    'NOTE': FNV_NOTESubrecords,
    'FACT': FNV_FACTSubrecords,
})
