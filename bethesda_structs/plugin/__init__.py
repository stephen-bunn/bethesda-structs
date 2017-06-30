#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import sys
import inspect

from ._common import AbstractPlugin
from .tes4 import TES4Plugin


def get_plugin(filepath: str) -> AbstractPlugin:
    """ Unreliable method of guessing and initializing a plugin \
        given a filepath.

    :param filepath: A filepath to a Bethesda plugin
    :type filepath: str
    :returns: An initialized plugin, hopefully
    """

    for (class_name, class_ref,) in \
            inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if class_ref not in (AbstractPlugin,) and \
                class_ref.can_handle(filepath):
            return class_ref(filepath)
