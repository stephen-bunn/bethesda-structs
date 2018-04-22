# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

import os

import pytest


STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


@pytest.fixture(scope="session", params=os.listdir(os.path.join(STATIC_DIR, "bsa/")))
def bsa_file(request):
    return os.path.join(STATIC_DIR, "bsa", request.param)


@pytest.fixture(scope="session", params=os.listdir(os.path.join(STATIC_DIR, "btdx/")))
def btdx_file(request):
    return os.path.join(STATIC_DIR, "btdx", request.param)


@pytest.fixture(
    scope="session",
    params=[
        ("DX10", 808540228),
        ("ATI2", 843666497),
        ("AAAA", 1094795585),
        ("ZZZZ", 1515870810),
    ],
)
def makefourcc_pair(request):
    return request.param
