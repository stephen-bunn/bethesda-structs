.. _getting-started:

===============
Getting Started
===============

| **Welcome to Bethesda-Structs!**
| This page should hopefully provide you with enough information to get you started interacting with some of Bethesda's file formats.

Installation and Setup
======================

Installing the package should be super duper simple as we utilize Python's setuptools.

.. code-block:: bash

   $ pipenv install bethesda-structs
   $ # or if you're old school...
   $ pip install bethesda-structs

Or you can build and install the package from the git repo.

.. code-block:: bash

   $ git clone https://github.com/stephen-bunn/bethesda-structs.git
   $ cd ./bethesda-structs
   $ python setup.py install


Example Usage
=============

| All of the supported file type classes are subclasses of :class:`~bethesda_structs._common.BaseFiletype`.
| These include :class:`~.archive._common.BaseArchive` and :class:`~.plugin._common.BasePlugin` and any other one-off file types.

Because this package is just a parser around some of Bethesda's popular file formats, its hopefully extendable to different purposes you might have.
Below are a few quick examples of how you might use this package, **but** remember to keep the :ref:`autodocs <bethesda-structs>` handy!


Checking if a file can be parsed
--------------------------------

Because many of the structures used to parse these filetypes are bulit using `construct <https://construct.readthedocs.io/en/latest/>`_, the parser **silently** fails if parsing raises an error.
For this reason, all file types include the classmethod :func:`~bethesda_structs._common.BaseFiletype.can_handle`, which takes a filepath and returns either ``True`` or ``False`` depending on if the filetype class believes it can parse the file.

This method can be executed similar to the following:

>>> from bethesda_structs.archive import BSAArchive
>>> BSAArchive.can_handle('/media/sf_VMShared/bsa/Campfire.bsa')
True
>>> from bethesda_structs.plugin import FNVPlugin
>>> FNVPlugin.can_handle('/media/sf_VMShared/bsa/Campfire.bsa')
False


Parsing a file
--------------

We try to keep the api simple and consistent across all of our parsable filetypes.
For example, the following methods should be available on all parseable filetypes:

   - :func:`~bethesda_structs._common.BaseFiletype.parse` — *parses bytes*
   - :func:`~bethesda_structs._common.BaseFiletype.parse_stream` — *parses bytes from a file stream*
   - :func:`~bethesda_structs._common.BaseFiletype.parse_file` — *parses bytes from a file path*

| This makes parsing of a given file super easy.
| For example:

>>> from bethesda_structs.archive import BSAArchive
>>> archive = BSAArchive.parse_file('/media/sf_VMShared/bsa/Campfire.bsa')
>>> archive
BSAArchive(filepath=PosixPath('/media/sf_VMShared/bsa/Campfire.bsa'))
>>> archive.filepath
PosixPath('/media/sf_VMShared/bsa/Campfire.bsa')

The ``filepath`` attribute is automatically transformed into a :class:`pathlib.Path` instance on initialization of the filetype.
This is really helpful for quickly obtaining file information if you need it.

>>> archive.filepath.stat()
os.stat_result(st_mode=33272, st_ino=6, st_dev=46, st_nlink=1, st_uid=0, st_gid=999, st_size=25097317, st_atime=1522860401, st_mtime=1522475016, st_ctime=1522475016)

.. note:: Parsed files *only* have the ``filepath`` attribute populated if either the :func:`~bethesda_structs._common.BaseFiletype.parse_file` method was used, or the ``filepath`` named argument was passed into the other parsing methods.


Examining a parsed file
-----------------------

All parsed files should contain the ``container`` attribute which is a root :class:`~construct.lib.Container` instance.
This contains the required information for examining a parsed file's contents.

For example you can view the header *sub*-container of a :class:`~.archive.bsa.BSAArchive` like the following:

>>> from bethesda_structs.archive import BSAArchive
>>> archive = BSAArchive.parse_file('/media/sf_VMShared/bsa/Campfire.bsa')
>>> print(archive.container.header)
Container:
    magic = b'BSA\x00' (total 4)
    version = 105
    directory_offset = 36
    archive_flags = Container:
        directories_named = True
        files_named = True
    directory_count = 4
    file_count = 493
    directory_names_length = 50
    file_names_length = 14839
    file_flags = Container:

| Every different subclass of :class:`~bethesda_structs._common.BaseFiletype` most likely implements a different ``container`` structure.
| For example, every :class:`~.archive.bsa.BSAArchive` has ``directory_records``, ``directory_blocks``, and ``file_names`` sub-containers:

>>> from bethesda_structs.archive import BSAArchive
>>> archive = BSAArchive.parse_file('/media/sf_VMShared/bsa/Campfire.bsa')
>>> print(archive.container.directory_records)
ListContainer:
    Container:
        hash = 1948419268744733541
        file_count = 155
        name_offset = 14971
    Container:
        hash = 2736503539341685349
        file_count = 174
        name_offset = 17467
    Container:
        hash = 3940292978845119603
        file_count = 163
        name_offset = 20268
    Container:
        hash = 11606842737777340531
        file_count = 1
        name_offset = 22885
>>> print(archive.container.directory_blocks[3])  # contains 1 file
Container:
    name = u'meshes\\mps\x00' (total 11)
    file_records = ListContainer:
        Container:
            hash = 16183754957220078963l
            size = 2384
            offset = 25094933
>>> print(archive.container.file_names[:5])
['_camp_objectplacementindicatorthread01.psc', '_camp_objectplacementindicatorthread02.psc', '_camp_objectplacementindicatorthread03.psc', '_camp_tentsitlayscript.psc', 'campcampfire.psc']

However, :class:`~.archive.btdx.BTDXArchive` has a completely different structure just using a ``files`` attribute.

>>> from bethesda_structs.archive import BTDXArchive
>>> archive = BTDXArchive.parse_file('/media/sf_VMShared/ba2/Immersive HUD - Main.bsa')
>>> print(archive.container.header)
Container:
    magic = b'BTDX' (total 4)
    version = 1
    type = u'GNRL' (total 4)
    file_count = 16
    names_offset = 39979
>>> print(archive.container.files[0])
Container:
    hash = 2246534376
    ext = u'swf' (total 3)
    directory_hash = 3539859571
    offset = 600
    packed_size = 0
    unpacked_size = 5011

**So knowledge of what you are parsing is important, but how it's being done shouldn't be.**

Extracting an archive
---------------------

All subclasses of :class:`~.archive._common.BaseArchive` contain a method :func:`~bethesda_structs.archive._common.BaseArchive.extract`.
This method makes it incredibly simple to extract the content of a parsed archive into a directory.

>>> from bethesda_structs.archive import BSAArchive
>>> archive = BSAArchive.parse_file('/media/sf_VMShared/bsa/Campfire.bsa')
>>> archive.extract('/home/stephen-bunn/Downloads/campfire-extracted/')
>>> from pathlib import Path
>>> for path in pathlib.Path('/home/stephen-bunn/Downloads/campfire-extracted/').glob('**/*'):
...    print(path.as_posix())
/home/stephen-bunn/Downloads/campfire-extracted/scripts/_camp_indicatortrigger.pexl
/home/stephen-bunn/Downloads/campfire-extracted/scripts/_camp_objectplacementthread30.pex
/home/stephen-bunn/Downloads/campfire-extracted/scripts/campconjuredshelter.pex
/home/stephen-bunn/Downloads/campfire-extracted/scripts/_camp_objectplacementindicatorthread02.pex
/home/stephen-bunn/Downloads/campfire-extracted/scripts/_camp_instinctseffects.pex
/home/stephen-bunn/Downloads/campfire-extracted/scripts/_camp_legacymenu.pex
/home/stephen-bunn/Downloads/campfire-extracted/scripts/_camp_objectplacementindicatorthread.pex
/home/stephen-bunn/Downloads/campfire-extracted/scripts/bladessparringscript.pex
/home/stephen-bunn/Downloads/campfire-extracted/scripts/tentsystem.pex
... <only first 9 files> ...


Both variants of :class:`~.archive.btdx.BTDXArchive` can also be extracted (``GNRL`` and ``DX10``).

Getting extraction progress
'''''''''''''''''''''''''''

The :func:`~bethesda_structs.archive._common.BaseArchive.extract` method takes a named argument ``progress_hook`` that acts as a (pre/post) callback function taking 3 positional arguments:

   - ``current`` — *current extracted bytes*
   - ``total`` — *total bytes to extract*
   - ``filepath`` — *current filepath being extracted*

>>> from bethesda_structs.archive import BSAArchive
>>> archive = BSAArchive.parse_file('/media/sf_VMShared/bsa/Campfire.bsa')
>>> def progress_hook(current, total, filepath):
...     print(((current / total) * 100.0, filepath))
>>> archive.extract('/home/stephen-bunn/Downloads/campfire-extracted/', progress_hook=progress_hook)
(0.0, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_objectplacementindicatorthread01.psc')
(0.0003748842843881753, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_objectplacementindicatorthread01.psc')
(0.0003748842843881753, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_objectplacementindicatorthread02.psc')
(0.0007497685687763506, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_objectplacementindicatorthread02.psc')
(0.0007497685687763506, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_objectplacementindicatorthread03.psc')
(0.0011246528531645259, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_objectplacementindicatorthread03.psc')
(0.0011246528531645259, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_tentsitlayscript.psc')
(0.004051940775940278, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/_camp_tentsitlayscript.psc')
(0.004051940775940278, '/home/stephen-bunn/Downloads/campfire-extracted/scripts/source/campcampfire.psc')
... <only first 9 callbacks> ...

Working with plugins
--------------------

So far in these quick examples we've only seen examples using archives, but we can also parse and examine plugins as well!
Well parsing these file types is done in the same way as archives.

>>> from bethesda_structs.plugin import FNVPlugin
>>> plugin = FNVPlugin.parse_file('/media/sf_VMShared/esp/fnv/NVWillow.esp')
>>> print(plugin.container.header)
Container:
    type = u'TES4' (total 4)
    data_size = 163
    flags = Container:
        master = True
    id = 0
    revision = 0
    version = 15
    data = b'HEDR\x0c\x00\x1f\x85\xab?\x97\x12\x00\x00#\xad'... (truncated, total 163)
    subrecords = ListContainer:
        Container:
            type = u'HEDR' (total 4)
            data_size = 12
            data = b'\x1f\x85\xab?\x97\x12\x00\x00#\xad\r\x00' (total 12)
            parsed = Container:
                value = Container:
                    version = 1.340000033378601
                    num_records = 4759
                    next_object_id = 896291
                description = u'Header' (total 6)
        Container:
            type = u'CNAM' (total 4)
            data_size = 9
            data = b'llamaRCA\x00' (total 9)
            parsed = Container:
                value = u'llamaRCA' (total 8)
                description = u'Author' (total 6)
        Container:
            type = u'SNAM' (total 4)
            data_size = 16
            data = b'NVWillow v.1.10\x00' (total 16)
            parsed = Container:
                value = u'NVWillow v.1.10' (total 15)
                description = u'Description' (total 11)
        Container:
            type = u'MAST' (total 4)
            data_size = 14
            data = b'FalloutNV.esm\x00' (total 14)
            parsed = Container:
                value = u'FalloutNV.esm' (total 13)
                description = u'Master Plugin' (total 13)
        Container:
            type = u'DATA' (total 4)
            data_size = 8
            data = b'\x00\x00\x00\x00\x00\x00\x00\x00' (total 8)
            parsed = Container:
                value = 0
                description = u'File Size' (total 9)
        Container:
            type = u'ONAM' (total 4)
            data_size = 68
            data = b'V\xe3\x0c\x00\xc3\xe3\x0c\x00\xc4\xe3\x0c\x00\xc5\xe3\x0c\x00'... (truncated, total 68)
            parsed = Container:
                value = ListContainer:
                    844630
                    844739
                    844740
                    844741
                    1372461
                    1372463
                    1383111
                    1385321
                    1387301
                    1387302
                    1387303
                    1387304
                    1387906
                    1457771
                    1479505
                    1520201
                    1544392
                description = u'Overridden Records' (total 18)


Getting plugin masters
''''''''''''''''''''''

One of the most common tasks in plugin analysis is determining the masters of a plugin.
The names of a plugin's masters are stored within the ``MAST`` subrecords in the plugin's header record.
Using the information above, you can get these names like the following:

>>> from bethesda_structs.plugin import FNVPlugin
>>> masters = []
>>> for subrecord in plugin.container.header.subrecords:
...     if subrecord.type == 'MAST':
...         masters.append(subrecord.parsed.value)
>>> print(masters)
['FalloutNV.esm']

You can also use the :func:`~bethesda_structs.plugin._common.BasePlugin.iter_subrecords` helper method to simplify your code:

>>> masters = [
...     subrecord.parsed.value
...     for subrecord in plugin.iter_subrecords(
...         'MAST', 'TES4',
...         include_header=True
...     )
... ]
>>> print(masters)
['FalloutNV.esm']


Getting key (``KEYM``) records
''''''''''''''''''''''''''''''

Here is a quick example at getting the data for the first ``KEYM`` record (an in-game key).
This probably really isn't that helpful to you, but I think an example was needed on how to iterate over specific records (as they can become quite large).

>>> from bethesda_structs.plugin import FNVPlugin
>>> for record in plugin.iter_records('KEYM'):
...     print(record)
...     break
Container:
    type = u'KEYM' (total 4)
    data_size = 279
    flags = Container:
    id = 17415634
    revision = 0
    version = 15
    data = b'EDID\x17\x00WillowNova'... (truncated, total 279)
    subrecords = ListContainer:
        Container:
            type = u'EDID' (total 4)
            data_size = 23
            data = b'WillowNovacBunga'... (truncated, total 23)
            parsed = Container:
                value = u'WillowNovacBungalowKey' (total 22)
                description = u'Editor ID' (total 9)
        Container:
            type = u'OBND' (total 4)
            data_size = 12
            data = b'\xff\xff\xfc\xff\x00\x00\x01\x00\x04\x00\x00\x00' (total 12)
            parsed = Container:
                value = Container:
                    X1 = -1
                    Y1 = -4
                    Z1 = 0
                    X2 = 1
                    Y2 = 4
                    Z2 = 0
                description = u'Object Bounds' (total 13)
        Container:
            type = u'FULL' (total 4)
            data_size = 27
            data = b'Dino Dee-lite Bu'... (truncated, total 27)
            parsed = Container:
                value = u'Dino Dee-lite Bungalow Key' (total 26)
                description = u'Name' (total 4)
        Container:
            type = u'MODL' (total 4)
            data_size = 23
            data = b'Clutter\\Key01Dir'... (truncated, total 23)
            parsed = Container:
                value = u'Clutter\\Key01Dirty.NIF' (total 22)
                description = u'Model Filename' (total 14)
        Container:
            type = u'ICON' (total 4)
            data_size = 48
            data = b'Interface\\Icons\\'... (truncated, total 48)
            parsed = Container:
                value = u'Interface\\Icons\\PipboyImages\\Ite'... (truncated, total 47)
                description = u'Large Icon Filename' (total 19)
        Container:
            type = u'MICO' (total 4)
            data_size = 66
            data = b'Interface\\Icons\\'... (truncated, total 66)
            parsed = Container:
                value = u'Interface\\Icons\\PipboyImages_sma'... (truncated, total 65)
                description = u'Small Icon Filename' (total 19)
        Container:
            type = u'SCRI' (total 4)
            data_size = 4
            data = b'T.\n\x01' (total 4)
            parsed = Container:
                value = FormID(form_id=17444436, forms=['SCPT'])
                description = u'Script' (total 6)
        Container:
            type = u'YNAM' (total 4)
            data_size = 4
            data = b'\xbb\x10\x07\x00' (total 4)
            parsed = Container:
                value = FormID(form_id=463035, forms=['SOUN'])
                description = u'Sound - Pick Up' (total 15)
        Container:
            type = u'ZNAM' (total 4)
            data_size = 4
            data = b'\xbc\x10\x07\x00' (total 4)
            parsed = Container:
                value = FormID(form_id=463036, forms=['SOUN'])
                description = u'Sound - Drop' (total 12)
        Container:
            type = u'DATA' (total 4)
            data_size = 8
            data = b'\x00\x00\x00\x00\x00\x00\x00\x00' (total 8)
            parsed = Container:
                value = Container:
                    value = 0
                    weight = 0.0
                description = u'Data' (total 4)

