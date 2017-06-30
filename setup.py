#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import os
import setuptools


REQUIREMENTS = []
with open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'requirements.txt'
), 'r') as fp:
    REQUIREMENTS = fp.readlines()


setuptools.setup(
    name='bethesda-structs',
    version='0.0.1',
    description=(
        'A wrapper for some of Bethesda\'s popular plugin/archive file formats'
    ),
    url='http://github.com/stephen-bunn/bethesda-structs',
    author='Stephen Bunn',
    author_email='stephen@bunn.io',
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
