# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import abc

from .. import meta


class AbstractPlugin(meta.CheckSummed, metaclass=abc.ABCMeta):
    """ A template class for all plugin structures.
    """

    def __eq__(self, other) -> bool:
        """ Evaluates if two plugins are equal.

        :param other: Another AbstractPlugin instance
        :type other: AbstractPlugin
        :returns: True if equal, otherwise False
        """

        return self.checksum() == other.checksum()

    @classmethod
    @abc.abstractmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a given filepath can be handled by this plugin.

        :param filepath: The filepath of a potential plugin
        :type filepath: str
        :returns: True if the plugin can handle it, otherwise False
        """

        raise NotImplementedError()
