#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT <https://opensource.org/licenses/MIT>

import abc
import hashlib


class CheckSummed(object, metaclass=abc.ABCMeta):
    """ A base for objects wrapping a file that can be summed.
    """

    _checksum_chunksize = (2 ** 10)

    @abc.abstractproperty
    def filepath(self) -> str:
        """ Required filepath for determining a checksum.

        :getter: Returns a filepath
        :setter: Does not allow setting
        """

        raise NotImplementedError()

    def checksum(self, algorithm: str='md5') -> str:
        """ Calculates a checksum for the file at the class's filepath.

        .. note:: Valid algorithm strings are the names of the \
            algorithm classes tied to the built-in :mod:`hashlib` module.

        :param algorithm: The hashing algorithm to utilize
        :type algorithm: str
        :returns: The checksum for the file at the class's filepath
        """

        algorithm = getattr(hashlib, algorithm)()
        with open(self.filepath, 'rb') as fp:
            while True:
                chunk = fp.read(self._checksum_chunksize)
                if not chunk:
                    break
                algorithm.update(chunk)
        return algorithm.hexdigest()