.. image:: https://github.com/stephen-bunn/bethesda-structs/raw/master/docs/source/_static/img/logo.png
   :alt: Bethesda Structs Logo
   :width: 800
   :align: center

.. image:: https://img.shields.io/pypi/v/bethesda-structs.svg
   :target: https://pypi.org/project/bethesda-structs/
   :alt: PyPi Status

.. image:: https://img.shields.io/pypi/pyversions/bethesda-structs.svg
   :target: https://pypi.org/project/bethesda-structs/
   :alt: Supported Versions

.. image:: https://img.shields.io/github/license/stephen-bunn/bethesda-structs.svg
   :target: https://github.com/stephen-bunn/bethesda-structs/blob/master/LICENSE
   :alt: License

.. image:: https://travis-ci.org/stephen-bunn/bethesda-structs.svg?branch=master
   :target: https://travis-ci.org/stephen-bunn/bethesda-structs
   :alt: Build Status

.. image:: https://img.shields.io/readthedocs/bethesda-structs.svg
   :target: https://bethesda-structs.readthedocs.io/
   :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/2546de38602c41aebddd94843760f968
   :target: https://www.codacy.com/app/stephen-bunn/bethesda-structs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=stephen-bunn/bethesda-structs&amp;utm_campaign=Badge_Grade
   :alt: Codacy Grade

.. image:: https://bethesda-structs-slackin.herokuapp.com/badge.svg
   :target: https://bethesda-structs-slackin.herokuapp.com/
   :alt: Slack

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/stephen-bunn
   :alt: Say Thanks!

.. image:: https://badge.waffle.io/stephen-bunn/bethesda-structs.svg?columns=all
   :target: https://waffle.io/stephen-bunn/bethesda-structs
   :alt: Waffle.io

----------

About
-----
| *Modding Bethesda's games can be a fine-art.*
| This package intends to provide **clean** and **accessible** methods for parsing and understanding Bethesda's filetypes.

*For example:*

There are so many "unarchiver" tools for Bethesda's archives (``.bsa`` and ``.ba2``), but no *good* programmatic way to read these filetypes.
Using this package, understanding **every little detail** about an archive is simple and straight-forward (see `BSA Usage`_ and `BA2 Usage`_).

For more advanced usage and information, `check out the documentation <https://bethesda-structs.readthedocs.io/>`_.

   | The supported filetypes are **parsers** not **writers**.
   | *We do not currently support the writing of archives or plugins.*


Installation
------------
Because this is glorious Python, installing ``bethesda-structs`` should be super-duper simple.

Using PyPi
''''''''''
The fastest and quickest way to install this packages is by simply using `pipenv <https://docs.pipenv.org/>`_ (or if you're oldschool `pip <https://pip.pypa.io/en/stable/quickstart/>`_).

.. code-block:: bash

   $ pipenv install bethesda-structs


Using Git
'''''''''
You can install this package using Git by simply cloning the repo and building the package yourself!

.. code-block:: bash

   $ git clone https://github.com/stephen-bunn/bethesda-structs.git
   $ pipenv install --dev
   $ pipenv run python setup.py install


Usage
-----
| Using ``bethesda-structs`` is designed to be straight-forward and intuitive.
| Below are some short examples of parsing various filetypes.


.. _ESP Usage:

ESP
'''
| The ability to parse plugin files is super helpful for understanding the additions and changes that are made to the game.
| Currently the **only** other real tool that can expose this information to you is `TESEdit <https://www.nexusmods.com/skyrim/mods/25859>`_ and its sibling applications.

This package aims to provide simple, programmatic access to the in-depth details of a plugin!

   Because of how long it takes to build complete subrecord parers for a given plugin version, the **only** currently supported plugins are:

   - ``FNVPlugin`` - Fallout: New Vegas (*partial*)
   - ``F03Plugin`` - Fallout 3 (*partial and experimental*)

>>> from bethesda_structs.plugin.fnv import FNVPlugin
>>> plugin = FNVPlugin.parse_file('/media/sf_VMShared/esp/fnv/NVWillow.esp')
>>> print(plugin)
FNVPlugin(filepath='/media/sf_VMShared/esp/fnv/NVWillow.esp')
>>>
>>> # print plugin header (is a record)
...
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
>>>
>>> # iterate over KEYM records (only 1 in this plugin)
...
>>> for record in plugin.iter_records('KEYM'):
...     print(record)
...
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


.. _BSA Usage:

BSA
'''
Bethesda's default archive structure.

>>> from bethesda_structs.archive.bsa import BSAArchive
>>> archive = BSAArchive.parse_file('/media/sf_VMShared/bsa/Campfire.bsa')
>>> print(archive)
BSAArchive(filepath=PosixPath('/media/sf_VMShared/bsa/Campfire.bsa'))
>>>
>>> # print archive header
...
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
>>>
>>> # print last directory block, containing 1 file record
...
>>> print(archive.container.directory_blocks[-1])
Container:
    name = u'meshes\\mps\x00' (total 11)
    file_records = ListContainer:
        Container:
            hash = 16183754957220078963
            size = 2384
            offset = 25094933
>>>
>>> # print archived filenames (only first 5, 488 more)
...
>>> print(archive.container.file_names)
ListContainer:
    _camp_objectplacementindicatorthread01.psc
    _camp_objectplacementindicatorthread02.psc
    _camp_objectplacementindicatorthread03.psc
    _camp_tentsitlayscript.psc
    campcampfire.psc
    ...
>>>
>>> # extract archive to directory
...
>>> archive.extract('/home/USER/Downloads')


.. _BA2 Usage:

BA2
'''
| Bethesda's second archive structure (used in Fallout 4).
| BTDX archives (BA2) are harder to extract than their previous version BA2.

The two available archive subtypes are both supported.

General (``GNRL``)
~~~~~~~~~~~~~~~~~~
Used to store generic files in a compressed/bundled file.

>>> from bethesda_structs.archive.btdx import BTDXArchive
>>> archive = BTDXArchive.parse_file('/media/sf_VMShared/ba2/CheatTerminal - Main.ba2')
>>> print(archive)
BTDXArchive(filepath=PosixPath('/media/sf_VMShared/ba2/CheatTerminal - Main.ba2'))
>>>
>>> # print archive header
...
>>> print(archive.container.header)
Container:
    magic = b'BTDX' (total 4)
    version = 1
    type = u'GNRL' (total 4)
    file_count = 982
    names_offset = 3600179
>>>
>>> # print first archive file entry
...
>>> print(archive.container.files[0])
Container:
    hash = 153050373
    ext = u'pex' (total 3)
    directory_hash = 1081231424
    offset = 35376
    packed_size = 0
    unpacked_size = 887
>>>
>>> # extract archive to directory
...
>>> archive.extract('/home/USER/Downloads')


Direct Draw (``DX10``)
~~~~~~~~~~~~~~~~~~~~~~
Used to store (specifically) Microsoft Direct Draw textures.

>>> from bethesda_structs.archive.btdx import BTDXArchive
>>> archive = BTDXArchive.parse_file('/media/sf_VMShared/ba2/AK74m - Textures.ba2')
>>> print(archive)
BTDXArchive(filepath=PosixPath('/media/sf_VMShared/ba2/AK74m - Textures.ba2'))
>>>
>>> # print archive header
...
>>> print(archive.container.header)
Container:
    magic = b'BTDX' (total 4)
    version = 1
    type = u'DX10' (total 4)
    file_count = 116
    names_offset = 329069673
>>>
>>> # print first archive file entry
...
>>> print(archive.container.files[0])
Container:
    header = Container:
        hash = 362144756
        ext = u'dds' (total 3)
        directory_hash = 1416395408
        chunks_count = 4
        chunk_header_size = 24
        height = 2048
        width = 2048
        mips_count = 12
        format = 99
    chunks = ListContainer:
        Container:
            offset = 11136
            packed_size = 2714729
            unpacked_size = 4194304
            start_mip = 0
            end_mip = 0
        Container:
            offset = 2725865
            packed_size = 840614
            unpacked_size = 1048576
            start_mip = 1
            end_mip = 1
        Container:
            offset = 3566479
            packed_size = 217598
            unpacked_size = 262144
            start_mip = 2
            end_mip = 2
        Container:
            offset = 3784077
            packed_size = 71579
            unpacked_size = 87408
            start_mip = 3
            end_mip = 11
>>>
>>> # extract archive to directory
...
>>> archive.extract('/home/USER/Downloads')
