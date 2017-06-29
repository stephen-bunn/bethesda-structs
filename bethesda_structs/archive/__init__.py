#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT <https://opensource.org/licenses/MIT>

import sys
import inspect

from ._common import AbstractArchive
from .bsa import BSAArchive


def get_archive(filepath: str) -> AbstractArchive:
    """ Unreliable method of guessing and initializing a archive \
        given a filepath.

    :param filepath: A filepath to a Bethesda archive
    :type filepath: str
    :returns: An initialized archive, hopefully
    """

    for (class_name, class_ref,) in \
            inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if class_ref not in (AbstractArchive,) and \
                class_ref.can_handle(filepath):
            return class_ref(filepath)
