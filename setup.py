#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import os
import setuptools

import bethesda_structs


REQUIREMENTS = []
with open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'requirements.txt'
), 'r') as fp:
    REQUIREMENTS = fp.readlines()


setuptools.setup(
    name=bethesda_structs.__name__,
    version=bethesda_structs.__version__,
    description=bethesda_structs.__description__,
    url='http://github.com/stephen-bunn/bethesda-structs',
    author=bethesda_structs.__author__,
    author_email=bethesda_structs.__contact__,
    license='MIT',
    packages=[
        'bethesda_structs',
        'bethesda_structs.meta',
        'bethesda_structs.plugin',
        'bethesda_structs.archive'
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': [
            'sphinx',
            'sphinx-autodoc-typehints',
            'sphinx-readable-theme',
        ]
    }
)
