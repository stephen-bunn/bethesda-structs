.. _bethesda-structs:

Bethesda Structs Package
========================
The following is the automatically built documentation for the entire :mod:`bethesda_structs` package.
All objects that are considered to be handlers for a Bethesda file format are subclasses of :class:`~._common.BaseFiletype`.

``Plugins`` and ``Archives`` adhere to the following naming conventions.
   - ``{GAME_PREFIX}Plugin`` - :class:`~.plugin.fnv.FNVPlugin`
   - ``{TYPE_PREFIX}Archive`` - :class:`~.archive.bsa.BSAArchive`

In some cases (such as :class:`~.archive.bsa.BSAArchive`) this may seem repetitive (``BSA[rchive]Archive``).
But, in this project, repetition is sacrificed for standardization.

.. important:: Common resources for each module (including submodules) are placed in a file named ``_common.py`` for each module. Typically you will see abstract objects or module helper methods defined in these files.

   They are important for **contributors**, but shouldn't ever need to be seen by users.

.. automodule:: bethesda_structs
   :members:
   :undoc-members:
   :show-inheritance:

.. toctree::

   Plugins <bethesda_structs.plugin>
   Archives <bethesda_structs.archive>
   Additional <bethesda_structs.contrib>

-----

.. automodule:: bethesda_structs._common
   :members:
   :undoc-members:
   :show-inheritance:
