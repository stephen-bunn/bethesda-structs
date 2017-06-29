#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT <https://opensource.org/licenses/MIT>

import abc
import struct
from typing import (Tuple,)


class Prefixed(object, metaclass=abc.ABCMeta):
    """ A base for objects with prefix structures.
    """

    @abc.abstractproperty
    def _prefix_struct(self) -> str:
        """ The required prefix struct format.

        :getter: Returns the required prefix struct format
        :setter: Does not allow setting
        """

        raise NotImplementedError()

    @abc.abstractproperty
    def _prefix_names(self) -> Tuple[str]:
        """ The required prefix name tuple.

        :getter: Returns the required prefix name tuple
        :setter: Does not allow setting
        """

        raise NotImplementedError()

    @property
    def _prefix_size(self) -> int:
        """ The size of the prefix in bytes.

        :getter: Returns the size of the prefix in bytes
        :setter: Does not allow setting
        """

        return struct.calcsize(self._prefix_struct)

    def __init__(self, buffer: bytes):
        """ Required initialization for prefixed objects.

        :param buffer: The archive buffer starting at the file object offset
        :type buffer: bytes
        """

        self._buffer = buffer

        for (name, value) in zip(
            self._prefix_names,
            struct.unpack(
                self._prefix_struct,
                self._buffer[:self._prefix_size]
            )
        ):
            setattr(self, name, value)