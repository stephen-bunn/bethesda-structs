#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT <https://opensource.org/licenses/MIT>

import os
import struct

from . import tes4


class TES5Plugin(tes4.TES4Plugin):
    """ Wrapper for a TES5 plugin.
    """

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a given filepath can be handled by this plugin.

        :param filepath: The filepath of a potential TES5 plugin
        :type filepath: str
        :returns: True if the plugin can handle it, otherwise False
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError((
                "no such file '{filepath}' exists"
            ).format(**locals()))
        with open(filepath, 'rb') as fp:
            try:
                header = tes4.TES4Record(fp.read(
                    struct.calcsize(tes4.TES4Record._prefix_struct)
                ))
                # should be able to handle the record if it's tagged as a TES4
                # and is version 131, hopefully...
                return (header.type == b'TES4') and (header.version == 131)
            except struct.error as exc:
                # catch if it can't even unpack the header
                pass
        return False
