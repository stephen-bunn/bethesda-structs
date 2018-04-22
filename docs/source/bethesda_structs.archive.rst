bethesda\_structs\.archive
==========================
This module contains structures that can read and extract Bethesda's archive file formats.

.. automodule:: bethesda_structs.archive
   :members:
   :undoc-members:


Common
------
Below is a listing of common objects, resources, etc. that can and are probably used throughout the other Archive objects.
An example of this is the :class:`~.archive._common.BaseArchive` class which provides an abstract class which all valid archives should extend.


.. automodule:: bethesda_structs.archive._common
   :members:


BSA Archives
------------
This module contains all the required structures to extract BSA archives.

.. automodule:: bethesda_structs.archive.bsa
   :members:
   :show-inheritance:


BTDX Archives
-------------
This module (along with :mod:`~.bethesda_structs.contrib.dds`) contains all the required structures to read and extract BTDX (.ba2) archives.

.. automodule:: bethesda_structs.archive.btdx
   :members:
   :show-inheritance:

