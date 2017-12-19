# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import sys
import inspect

from ._common import (AbstractArchive,)
from .bsa import (BSAArchive,)
from .ba2 import (BA2Archive,)


def get_archive(filepath: str) -> AbstractArchive:
    """ Unreliable method of guessing and initializing a archive \
        given a filepath.

    :param filepath: A filepath to a Bethesda archive
    :type filepath: str
    :returns: An initialized archive, hopefully
    """

    # iterate over all the imported archives
    for (class_name, class_ref,) in \
            inspect.getmembers(sys.modules[__name__], inspect.isclass):
        # return the first archive that can handle the file
        # and isn't an abstract class
        if class_ref not in (AbstractArchive,) and \
                class_ref.can_handle(filepath):
            return class_ref(filepath)
