# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

from bethesda_structs.archive.bsa import BSAArchive
from bethesda_structs.archive._common import BaseArchive
from bethesda_structs._common import BaseFiletype


def test_subclass():
    assert issubclass(BSAArchive, BaseArchive)
    assert issubclass(BSAArchive, BaseFiletype)


def test_can_handle(bsa_file):
    assert BSAArchive.can_handle(bsa_file)
