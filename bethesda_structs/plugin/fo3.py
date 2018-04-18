# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://opensource.org/licenses/MIT>

from .fnv import FNVPlugin, FNVFormID


class FO3FormID(FNVFormID):
    """A formid wrapper for Fallout 3.

    Note:
        Because the logic for parsing Fallout 3 form ids is the same as
        Fallout: New Vegas form ids, this class is simply a subclass of
        :class:`~.plugin.fnv.FNVFormID`.

    **Credit:**
        - `FopDoc <https://tes5edit.github.io/fopdoc/FalloutNV/Records.html>`_
    """

    pass


class FO3Plugin(FNVPlugin):
    """The plugin for Fallout 3.

    Note:
        Because the logic for parsing Fallout 3 plugins is the same as
        Fallout: New Vegas plugins, this class is simply a subclass of
        :class:`~.plugin.fnv.FNVPlugin`.

    **Credit:**
        - `FopDoc <https://tes5edit.github.io/fopdoc/FalloutNV/Records.html>`_
    """

    pass
