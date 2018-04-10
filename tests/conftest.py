# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os

import pytest


STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


@pytest.fixture(scope="session", params=os.listdir(os.path.join(STATIC_DIR, 'bsa/')))
def bsa_file(request):
    return os.path.join(STATIC_DIR, 'bsa', request.param)
