# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from ._common import BasePlugin
from .fnv import FNVPlugin
from .fo3 import FO3Plugin

AVAILABLE_PLUGINS = (FNVPlugin, FO3Plugin)


def get_plugin(filepath: str) -> BasePlugin:
    """Get an instance of the first plugin that can handle a given file.

    Args:
        filepath (str): The path of the file to handle

    Returns:
        BasePlugin: The base plugin

    Examples:
        This method simply returns the first encountered plugin that can handle a
        given file.

        >>> FILEPATH = ""  # absolute filepath to some FNV plugin
        >>> plugin = bethesda_structs.plugin.get_plugin(FILEPATH)
        >>> plugin
        FNVPlugin(filepath=PosixPath(...))
    """

    for plug in AVAILABLE_PLUGINS:
        if plug.can_handle(filepath):
            return plug.parse_file(filepath)
