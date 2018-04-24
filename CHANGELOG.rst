=========
Changelog
=========

| All notable changes to this project will be documented in this file.
| The format is based on `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.
|

**WIP: 1.0.0** (*unreleased*)
-----------------------------

`0.1.3`_ (*2018-04-22*)
-----------------------
- full rewrite using `construct <https://construct.readthedocs.io/en/latest/>`_.
- added complete support for BTDX archives
- added complete support for BSA archives (*not including Morrowind*)
- added initial support for FNV plugins
- added basic support for subrecord structure parsing (*not easy* 😢)
- added initial archive tests 👨‍🔬
- added fancy new logos and badges 😄
- added beginnings of generic structure documentation
- **deprecated** all old structures and files from versions ``<0.1.0`` 👍

-----

`0.0.1`_ (*2018-01-12*)
-----------------------
- added basic UserWarning for WIP TES5 plugins


`0.0.0`_ (*2017-12-19*)
-----------------------
*this is the first pre-alpha release, so the only other prior change history is the git commit log*

- added initial support for TES4 plugins
- added initial support for *basic* TES5 plugins
- added initial support for BSA archives
- added initial support for BA2 archives
- added guess-work methods for guessing plugin/archive objects from a file
- added abstract class for checksumming classes with filepaths
- added abstract class for auto handling structures with prefixes
- added all of the documentations 😍


.. _0.0.0: https://github.com/stephen-bunn/bethesda-structs/releases/tag/v0.0.0
.. _0.0.1: https://github.com/stephen-bunn/bethesda-structs/releases/tag/v0.0.1
.. _0.1.2: https://github.com/stephen-bunn/bethesda-structs/releases/tag/v0.1.2
