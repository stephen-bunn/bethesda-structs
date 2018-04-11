# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

from bethesda_structs.contrib.dds import MAKEFOURCC
from construct import Bytes, Int32ul


def test_MAKEFOURCC(makefourcc_pair):
    assert MAKEFOURCC(*makefourcc_pair[0]) == makefourcc_pair[-1]
