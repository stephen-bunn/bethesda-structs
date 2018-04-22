# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from bethesda_structs.contrib.dds import MAKEFOURCC
from construct import Bytes, Int32ul


def test_MAKEFOURCC(makefourcc_pair):
    assert MAKEFOURCC(*makefourcc_pair[0]) == makefourcc_pair[-1]
