bethesda\_structs\.plugin
=========================
This module contains structures that can read and extract Bethesda's plugin file formats.
These are files typically denoted with the following extensions:

   - ``.esp`` - *Elder Scrolls Plugin*
   - ``.esm`` - *Elder Scrolls Master*
   - ``.esl`` - *Elder Scrolls Light*

These files contain and register logic and resources in order to extend the content and logic of an "Elder Scrolls" (engine) game.
Typically the frontline of runtime errors, being able to understand what data the plugin contains is critical to understanding how to fix errors.

.. automodule:: bethesda_structs.plugin
   :members:
   :undoc-members:
   :show-inheritance:

Common
------
Below is a listing of common objects, resources, etc. that can are are probably used throughout the other Plugin objects.
An example of this is the :class:`~.plugin._common.BasePlugin` class which provides an abstract class which all valid plugins should extend.

.. automodule:: bethesda_structs.plugin._common
   :members:


Fallout: New Vegas
------------------
This module contains all the required structures to parse FNV plugins.

.. automodule:: bethesda_structs.plugin.fnv
   :members:
   :undoc-members:
   :show-inheritance:


Fallout 3
---------
This module contains all the required structures to parse FO3 plugins.

.. automodule:: bethesda_structs.plugin.fo3
   :members:
   :undoc-members:
   :show-inheritance:
