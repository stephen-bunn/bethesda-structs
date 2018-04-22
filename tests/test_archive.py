# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from bethesda_structs.archive import get_archive, AVAILABLE_ARCHIVES
from bethesda_structs.archive.bsa import BSAArchive
from bethesda_structs.archive.btdx import BTDXArchive


def test_bsa_get_archive(bsa_file):
    arch = get_archive(bsa_file)
    assert arch is not None
    assert arch.__class__ in AVAILABLE_ARCHIVES
    assert isinstance(arch, BSAArchive)


def test_btdx_get_archive(btdx_file):
    arch = get_archive(btdx_file)
    assert arch is not None
    assert arch.__class__ in AVAILABLE_ARCHIVES
    assert isinstance(arch, BTDXArchive)
