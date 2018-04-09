# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

from ._common import BaseArchive
from .bsa import BSAArchive
from .btdx import BTDXArchive

AVAILABLE_ARCHIVES = (BSAArchive, BTDXArchive,)


def get_archive(filepath: str) -> BaseArchive:
    for arch in AVAILABLE_ARCHIVES:
        if arch.can_handle(filepath):
            return arch.parse_file(filepath)
