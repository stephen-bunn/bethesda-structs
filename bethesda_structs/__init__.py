# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

from typing import (Union,)

from . import (plugin, archive,)


def get_struct(filepath: str) -> \
        Union[plugin.AbstractPlugin, archive.AbstractArchive]:
    """ Unreliable method of guessing and initalizing the struct \
        from a filepath.

    :param filepath: A filepath to a Bethesda formatted file
    :type filepath: str
    :returns: A struct which can handle the file, hopefully
    """

    struct_ = plugin.get_plugin(filepath)
    if struct_:
        return struct_
    return archive.get_archive(filepath)
