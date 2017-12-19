================
Bethesda Structs
================

|

.. image:: https://img.shields.io/pypi/v/bethesda-structs.svg
   :target: https://pypi.org/project/bethesda-structs/
   :alt: PyPi Status

.. image:: https://img.shields.io/pypi/pyversions/bethesda-structs.svg
   :target: https://pypi.org/project/bethesda-structs/
   :alt: Supported Versions

.. image:: https://img.shields.io/pypi/status/bethesda-structs.svg
   :target: https://pypi.org/project/bethesda-structs/
   :alt: Release Status

.. image:: https://img.shields.io/github/last-commit/stephen-bunn/bethesda-structs.svg
   :target: https://github.com/stephen-bunn/bethesda-structs
   :alt: Last Commit

.. image:: https://img.shields.io/github/license/stephen-bunn/bethesda-structs.svg
   :target: https://github.com/stephen-bunn/bethesda-structs/blob/master/LICENSE
   :alt: License

.. image:: https://readthedocs.org/projects/bethesda-structs/badge/?version=latest
   :target: http://bethesda-structs.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/stephen-bunn/bethesda-structs.svg?branch=master
   :target: https://travis-ci.org/stephen-bunn/bethesda-structs
   :alt: Build Status

.. image:: https://requires.io/github/stephen-bunn/bethesda-structs/requirements.svg?branch=master
   :target: https://requires.io/github/stephen-bunn/bethesda-structs/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/stephen-bunn
   :alt: Say Thanks

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
