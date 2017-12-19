# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import sys
import inspect

from ._common import (AbstractPlugin,)
from .tes4 import (TES4Plugin,)
from .tes5 import (TES5Plugin,)


def get_plugin(filepath: str) -> AbstractPlugin:
    """ Unreliable method of guessing and initializing a plugin \
        given a filepath.

    :param filepath: A filepath to a Bethesda plugin
    :type filepath: str
    :returns: An initialized plugin, hopefully
    """

    # iterate over all the imported plugins
    for (class_name, class_ref,) in \
            inspect.getmembers(sys.modules[__name__], inspect.isclass):
        # return the first plugin that can handle the file
        # and isn't an abstract class
        if class_ref not in (AbstractPlugin,) and \
                class_ref.can_handle(filepath):
            return class_ref(filepath)
