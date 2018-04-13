# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from pathlib import Path

from bethesda_structs._common import BaseFiletype
from bethesda_structs.archive.btdx import BTDXArchive
from bethesda_structs.archive._common import ArchiveFile, BaseArchive


def test_subclass():
    assert issubclass(BTDXArchive, BaseArchive)
    assert issubclass(BTDXArchive, BaseFiletype)


def test_can_handle(btdx_file):
    assert BTDXArchive.can_handle(btdx_file)


def test_iter_files(btdx_file):
    arch = BTDXArchive.parse_file(btdx_file)
    for arch_file in arch.iter_files():
        assert isinstance(arch_file, ArchiveFile)
        assert isinstance(arch_file.filepath, Path)
        assert isinstance(arch_file.data, bytes)
        assert len(arch_file.data) > 0
