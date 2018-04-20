.. image:: https://github.com/stephen-bunn/bethesda-structs/raw/feature/construct/docs/source/_static/img/logo.png
   :alt: Bethesda Structs Logo
   :width: 800
   :align: center

.. raw:: html

   <p align="center">
      <a href="https://pypi.org/project/bethesda-structs/" target="_blank"><img alt="PyPi Status" src="https://img.shields.io/pypi/v/bethesda-structs.svg"></a>
      <a href="https://pypi.org/project/bethesda-structs/" target="_blank"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/bethesda-structs.svg"></a>
      <a href="https://github.com/stephen-bunn/bethesda-structs/blob/master/LICENSE" target="_blank"><img alt="License" src="https://img.shields.io/github/license/stephen-bunn/bethesda-structs.svg"></a>
      <a href="https://travis-ci.org/stephen-bunn/bethesda-structs" target="_blank"><img alt="Build Status" src="https://travis-ci.org/stephen-bunn/bethesda-structs.svg?branch=master"></a>
      <a href="http://bethesda-structs.readthedocs.io/" target="_blank"><img alt="Documentation Status" src="https://img.shields.io/readthedocs/bethesda-structs.svg"></a>
      <a href="https://www.codacy.com/app/stephen-bunn/bethesda-structs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=stephen-bunn/bethesda-structs&amp;utm_campaign=Badge_Grade" target="_blank"><img src="https://api.codacy.com/project/badge/Grade/2546de38602c41aebddd94843760f968"/></a>
      <a href="https://bethesda-structs-slackin.herokuapp.com/" target="_blank"><img alt="Slack" src="https://bethesda-structs-slackin.herokuapp.com/badge.svg"></a>
      <a href="https://saythanks.io/to/stephen-bunn" target="_blank"><img alt="Say Thanks!" src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg"></a>
      <a href="https://app.gitkraken.com/glo/oboard/Ws5Y0LAkoBEAfVcf" target="_blank"><img alt="Gitkraken: Glo" src="https://img.shields.io/badge/-Glo-212121.svg?longCache=true&colorA=212121&style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAMAAAAR8Wy4AAAC/VBMVEURg3cSgngQgHYRgnkA/wASgHkShHgRg3gThXkRgXgSg3YSgHkAf38AqlUAf38Sg3YSgHkSgHkSf38PgHkAf38Zf38Pg3YPg3YAmWYAkW0ff38Vf38SgHkcjXESg3YSgHYPg3YPh3gSgHkSgHcPg3YSgHcWhXkSg3cPgHkPgHkRiHcXi3MRgnoPf38SgnkPg3kOf38TiXUShXkXf3MSg3gQhHoUhngQgXkRgncSgncMhXkRgXgNhngPgHYSg3kQg3sVf3QSf3YSgHkRg3kQg3gTf3URgncPg3sSgHYPg3kSgXkSg3kSgnkSg3kSgnkSgnYRhHoPg3kSg3cSg3kQgnkSg3gMf3IRg3kRgnkSgXgPf3cSg3kQg3gTg3cShHoRgnkPgnYSg3gSgnoSg3kPg3kPf3gRgnYQhXkThHoPgHYRg3gSgXgSg3kSgncSg3kTgngSg3gRgXgPgXgUgngQg3cQg3gRgnkSg3gSgXkQgXgSgHgQg3kSg3kSgnYRg3kSg3gUgnwSgXkQg3gQgnkSgnkRgnkSgncQgXkRg3kRgnkRgngShHgRg3gRg3kSgnkPhHoTgXkSgngRf3cQgXkRgnkOg3sSg3kUhHoRhXkThHcSg3kRgncQgncSg3kRg3gSg3gTgnwSg3kRgnkTgnkSg3YSg3kQg3kQgncShHoTgXgSgngRg3kQgXgQg3gShHoRg3kSgXgRgXkTgXkRgngSgnoSgXgVf3gRg3kRg3gRg3gPgnYTg3kSgnkSg3kQgXkRg3cSg3gRg3kRgnkRhHoRgngSgnkQgnkSgnkPgncRg3kRg3kRgXoRg3kRg3gRg3gRg3sRgngRg3kRg3cSgXkRgXkShHgSg3gSgncSg3cRgXkRg3sSg3gSg3kRgnkSgngSgngRg3cSgngQg3cSgnkRgngSg3kSgngRgnkSg3kRgXgRgXgTg3gSgngShHcUhHoRg3gSgnoShHcTg3cSg3gRgngSgXgSg3kRg3kQgngSg3gRg3cSg3kSg3kSgnkSg3mHY0CZAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfiBAsUBxdiZClEAAAAQklEQVQI142PUQ4AIAhCuf+hXQairq9cTXizSUBW5Ak2Ff0i5U1IDa6NHpAimIk/UKv2SjhHaTxSTbHWe1//ppPiAG4xZzEYPXVzAAAAAElFTkSuQmCC"></a>
   </p>
   <p align="center">
      <a href="https://www.python.org/" target="_blank"><img alt="Made with: Python" src="https://forthebadge.com/images/badges/made-with-python.svg"></a>
   </p>


| A **real** and **usable** parser for some of Bethesda's file formats.
| Read about more complex usage in the `documentation <https://bethesda-structs.readthedocs.io/en/latest/>`_.
|


Extracting a BSA archive
------------------------

.. code-block:: python

   import os
   import bethesda_structs

   BSA_ARCHIVE_PATH = 'C:/Users/me/Desktop/Archive.bsa'
   EXTRACT_TO_DIR   = 'C:/Users/me/Desktop/ArchiveContents/'

   archive = bethesda_structs.archive.BSAArchive.parse_file(BSA_ARCHIVE_PATH)

   if not os.path.isdir(EXTRACT_TO_DIR):
       os.makedirs(EXTRACT_TO_DIR)

   archive.extract(EXTRACT_TO_DIR)


Display masters of a FNV plugin
-------------------------------

.. code-block:: python

   import os
   import bethesda_structs

   FNV_PLUGIN_PATH = 'C:/Users/me/Desktop/Plugin.esp'

   plugin = bethesda_structs.plugin.FNVPlugin.parse_file(FNV_PLUGIN_PATH)
   for subrecord in plugin.container.header:
      if subrecord.type == 'MAST':
         print(subrecord.parsed)
