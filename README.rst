================
Bethesda Structs
================

|

.. raw:: html

   <p align="center">
      <a href="https://pypi.org/project/bethesda-structs/" target="_blank"><img alt="PyPi Status" src="https://img.shields.io/pypi/v/bethesda-structs.svg"></a>
      <a href="https://pypi.org/project/bethesda-structs/" target="_blank"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/bethesda-structs.svg"></a>
      <a href="https://github.com/stephen-bunn/bethesda-structs/blob/master/LICENSE" target="_blank"><img alt="License" src="https://img.shields.io/github/license/stephen-bunn/bethesda-structs.svg"></a>
      <a href="http://bethesda-structs.readthedocs.io/en/latest/?badge=latest" target="_blank"><img alt="Documentation Status" src="https://readthedocs.org/projects/bethesda-structs/badge/?version=latest"></a>
      <a href="https://travis-ci.org/stephen-bunn/bethesda-structs" target="_blank"><img alt="Build Status" src="https://travis-ci.org/stephen-bunn/bethesda-structs.svg?branch=master"></a>
      <a class="badge-align" href="https://www.codacy.com/app/stephen-bunn/bethesda-structs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=stephen-bunn/bethesda-structs&amp;utm_campaign=Badge_Grade" target="_blank"><img src="https://api.codacy.com/project/badge/Grade/2546de38602c41aebddd94843760f968"/></a>
      <a href="https://github.com/ambv/black" target="_blank"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
   </p>

|


Usage
-----

| Inspect and extract Bethesda's TES4, TES5, BSA, and BA2 filetypes...
| Read about more complex usage in the `documentation <https://bethesda-structs.readthedocs.io/en/latest/>`_.
|


Extracting a BSA archive
''''''''''''''''''''''''

.. code-block:: python

   import os
   import bethesda_structs

   BSA_ARCHIVE_PATH = 'C:/Users/me/Desktop/Archive.bsa'
   EXTRACT_TO_DIR   = 'C:/Users/me/Desktop/ArchiveContents/'

   archive = bethesda_structs.archive.BSAArchive(BSA_ARCHIVE_PATH)

   if not os.path.isdir(EXTRACT_TO_DIR):
       os.makedirs(EXTRACT_TO_DIR)

   archive.extract(EXTRACT_TO_DIR)


Getting masters of a TES4 plugin
''''''''''''''''''''''''''''''''

.. code-block:: python

   import os
   import bethesda_structs

   TES_PLUGIN_PATH = 'C:/Users/me/Desktop/Archive.esp'

   plugin = bethesda_structs.plugin.get_plugin(TES_PLUGIN_PATH)
   print([
       field.data
       for field in plugin.header.fields
       if feild.type == b'MAST'
   ])
