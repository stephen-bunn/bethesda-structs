.. _getting-started-page:

===============
Getting Started
===============

This page should hopefully guide you to a point where you can start utilizing this package for analyzing and processing some of Bethesda's file formats.

Installation and Setup
======================

Installing the package should be super duper simple as we utilize Python's setuptools.

Bethesda Structs is not yet on PyPI as it is still undergoing initial development.
However, you can install Bethesda Structs by cloning the source and installing the package through the included setup script!

.. code-block:: bash

    $ git clone https://github.com/stephen-bunn/bethesda-structs.git
    $ cd ./bethesda-structs
    $ python setup.py install


Example Usage
=============

Because this package is a wrapper around some of Bethesda's popular file formats, it is hopefully extendable to different purposes you might have.

Below are a few quick examples of how you might use this package, **but** remember to keep the :ref:`modules-page` index handy!


Extracting an archive
---------------------

Lets say that you want to extract the contents of a BSA archive to a directory.
This can be done quickly using a snippet like the following:

.. code-block:: python

    import os
    import bethesda_structs

    BSA_ARCHIVE_PATH = 'C:/Users/me/Desktop/Archive.bsa'
    EXTRACT_TO_DIR   = 'C:/Users/me/Desktop/ArchiveContents/'

    archive = bethesda_structs.archive.BSAArchive(BSA_ARCHIVE_PATH)

    if not os.path.isdir(EXTRACT_TO_DIR):
        os.makedirs(EXTRACT_TO_DIR)

    archive.extract(EXTRACT_TO_DIR)

Because the archive package is `somewhat` smart, we can make a guess for the correct archive object by using the archive package's :func:`~bethesda_structs.archive.get_archive` method.

This method can be used to replace the line

.. code-block:: python

    archive = bethesda_structs.archive.BSAArchive(BSA_ARCHIVE_PATH)

with the simplification

.. code-block:: python

    archive = bethesda_structs.archive.get_archive(BSA_ARCHIVE_PATH)

This automatically handles the instance where ``BSA_ARCHIVE_PATH`` isn't actually pointing to a BSA archive.
Instead, it will set the local ``archive`` variable to whatever archive it thinks can handle the file.

*If no archive wrapper thinks it can handle the file, it will just set* ``archive`` *to* ``None``.

---

The BSA archive's :func:`~bethesda_structs.archive.bsa.BSAArchive.extract` method also comes with a **simple** progress hook callback!
This allows the user to somewhat visualize the progress of the extraction.

You can hook into the extraction progress callback by doing something similar to the following:

.. code-block:: python

    def _progress_hook(current, total, filepath):
        sys.stdout.write((
            '[{current}/{total}]: {filepath}\r\b'
        ).format(**locals()))
        sys.stdout.flush()

    archive.extract(EXTRACT_TO_DIR, hook=_progress_hook)
    sys.stdout.write('\n')

Your progress hook should take the ``current`` file number being extracted, the ``total`` number of files to be extracted, and the ``filepath`` where the file is being extracted to.
`Your progress hook could also be cooler than this nasty little hook.`

---

And guess what, **BA2 archives** are also supported!
Simply give the path to a BA2 archive and decompress and extract the archived contents out to a given directory!

.. code-block:: python

    BA2_ARCHIVE_PATH = 'C:/Users/me/Desktop/Archive.ba2'

    archive = bethesda_structs.archive.get_archive(BA2_ARCHIVE_PATH)

    if not os.path.isdir(EXTRACT_TO_DIR):
        os.makedirs(EXTRACT_TO_DIR)

    archive.extract(EXTRACT_TO_DIR)


List Masters of a TES Plugin
----------------------------

One of the most common tasks in plugin analysis is determining the masters of a plugin.
The names of a plugin's masters are stored within the ``MAST`` fields in the plugin's header record.
You can get a list of these names like this:

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
